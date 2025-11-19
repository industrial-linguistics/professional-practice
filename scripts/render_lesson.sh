#!/usr/bin/env bash
set -euo pipefail

# Render a single lesson into narrated video assets.
# Usage: PART=part-01 TOPIC=overview scripts/render_lesson.sh

PART=${PART:-}
TOPIC=${TOPIC:-}
VOICE=${VOICE:-Greg}
OUTPUT_ROOT=${OUTPUT_ROOT:-build}
CACHE_BUCKET=${CACHE_BUCKET:-${VOICER_S3_BUCKET:-}}
UPLOAD_BUCKET=${UPLOAD_BUCKET:-${LESSON_S3_BUCKET:-}}

if [[ -z "$PART" || -z "$TOPIC" ]]; then
  echo "PART and TOPIC environment variables are required" >&2
  exit 1
fi

root_dir=$(cd "$(dirname "$0")/.." && pwd)
content_dir="$root_dir/content/$PART/$TOPIC"
slides_file="$content_dir/slides.md"
narrative_dir="$content_dir/narratives"
image_dir="$root_dir/assets/slide-images/$PART/$TOPIC"
lesson_dir="$root_dir/$OUTPUT_ROOT/$PART/$TOPIC"
audio_dir="$lesson_dir/audio"
video_dir="$lesson_dir/video"
manifests_dir="$lesson_dir/manifests"

mkdir -p "$audio_dir" "$video_dir" "$manifests_dir"

if [[ ! -f "$slides_file" ]]; then
  echo "Missing slides file: $slides_file" >&2
  exit 1
fi
if [[ ! -d "$narrative_dir" ]]; then
  echo "Missing narrative directory: $narrative_dir" >&2
  exit 1
fi

normalize() {
  tr '\n' ' ' | tr -s '[:space:]' ' ' | sed 's/^ *//;s/ *$//'
}

format_ts() {
  python - "$1" <<'PY'
import sys
secs=float(sys.argv[1])
h=int(secs//3600); m=int((secs%3600)//60); s=secs%60
print(f"{h:02d}:{m:02d}:{s:06.3f}")
PY
}

narrative_files=($(find "$narrative_dir" -type f -name '*.md' | sort))
if [[ ${#narrative_files[@]} -eq 0 ]]; then
  echo "No narrative files found in $narrative_dir" >&2
  exit 1
fi

vtt_file="$manifests_dir/narration.vtt"
audio_manifest="$manifests_dir/audio-manifest.txt"
slide_manifest="$manifests_dir/slide-manifest.ffconcat"
timing_manifest="$manifests_dir/timings.tsv"

: >"$vtt_file"
: >"$audio_manifest"
: >"$timing_manifest"

prev_text=""
start_time=0
index=1

echo "WEBVTT" >"$vtt_file"

for i in "${!narrative_files[@]}"; do
  file="${narrative_files[$i]}"
  text=$(cat "$file" | normalize)
  next_text=""
  if [[ $((i+1)) -lt ${#narrative_files[@]} ]]; then
    next_text=$(cat "${narrative_files[$((i+1))]}" | normalize)
  fi
  context="$prev_text ||| $next_text"
  hash=$(printf "%s\n%s\n%s" "$VOICE" "$text" "$context" | sha256sum | awk '{print $1}')
  audio_file="$audio_dir/$hash.wav"

  if [[ ! -f "$audio_file" ]]; then
    if command -v voicer >/dev/null 2>&1; then
      args=(--say "$text" --voice "$VOICE" --output "$audio_file" --format pcm_44100 --autopad)
      if [[ -n "$CACHE_BUCKET" ]]; then
        args+=(--s3-bucket "$CACHE_BUCKET")
      fi
      echo "[voicer] Rendering $(basename "$file") -> $(basename "$audio_file")"
      voicer "${args[@]}"
    else
      words=$(echo "$text" | wc -w | awk '{print $1}')
      approx=$(python - "$words" <<'PY'
import sys
words=int(sys.argv[1]);
# assume 150 wpm with 0.5s buffer
secs=max(1.0, words/2.5 + 0.5)
print(f"{secs:.2f}")
PY
)
      echo "[fallback] Synthesizing silence for $(basename "$file") (${approx}s)"
      ffmpeg -loglevel warning -y -f lavfi -i anullsrc=r=44100:cl=mono -t "$approx" "$audio_file"
    fi
  fi

  duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio_file")
  end_time=$(python - "$start_time" "$duration" <<'PY'
import sys
start=float(sys.argv[1]); dur=float(sys.argv[2])
print(f"{start+dur:.3f}")
PY
)
  printf "\n%d\n%s --> %s\n%s\nNOTE context: prev=%s next=%s\n" "$index" "$(format_ts "$start_time")" "$(format_ts "$end_time")" "$text" "$prev_text" "$next_text" >>"$vtt_file"
  printf "%s\t%s\t%s\t%s\n" "$(basename "$file")" "$hash" "$duration" "$text" >>"$timing_manifest"
  printf "file '%s'\n" "$audio_file" >>"$audio_manifest"

  prev_text="$text"
  start_time=$end_time
  index=$((index+1))
done

echo "ffconcat version 1.0" >"$slide_manifest"
slide_images=($(find "$image_dir" -maxdepth 1 -type f -name 'slide.*.png' | sort))
if [[ ${#slide_images[@]} -eq 0 ]]; then
  echo "No slide images found in $image_dir" >&2
  exit 1
fi

# Align slide durations with audio durations; reuse last duration if counts differ
mapfile -t durations < <(cut -f3 "$timing_manifest")
for idx in "${!slide_images[@]}"; do
  dur_index=$idx
  if [[ $dur_index -ge ${#durations[@]} ]]; then
    dur_index=$((${#durations[@]}-1))
  fi
  dur=${durations[$dur_index]}
  printf "file %s\n" "${slide_images[$idx]}" >>"$slide_manifest"
  printf "duration %s\n" "$dur" >>"$slide_manifest"
done

narration="$video_dir/narration.wav"
silent_video="$video_dir/silent.mp4"
final_video="$video_dir/final.mp4"

ffmpeg -loglevel warning -y -f concat -safe 0 -i "$audio_manifest" -c copy "$narration"
ffmpeg -loglevel warning -y -safe 0 -f concat -i "$slide_manifest" \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -pix_fmt yuv420p -r 30 "$silent_video"
ffmpeg -loglevel warning -y -i "$silent_video" -i "$narration" -c:v libx264 -preset veryfast -pix_fmt yuv420p -c:a aac -shortest "$final_video"

if [[ -n "$UPLOAD_BUCKET" && -x "$(command -v aws)" ]]; then
  target="${UPLOAD_BUCKET%/}/$PART/$TOPIC"
  echo "Uploading assets to $target"
  aws s3 cp "$final_video" "$target/final.mp4"
  aws s3 cp "$narration" "$target/narration.wav"
  aws s3 cp "$vtt_file" "$target/narration.vtt"
  aws s3 cp "$timing_manifest" "$target/timings.tsv"
fi

cat <<SUMMARY
Rendered lesson $PART/$TOPIC
- Voice: $VOICE
- Narration manifest: $audio_manifest
- Slide manifest: $slide_manifest
- Final video: $final_video
SUMMARY
