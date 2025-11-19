#!/usr/bin/env bash
set -euo pipefail

VOICE=${VOICE:-Greg}
OUTPUT_ROOT=${OUTPUT_ROOT:-build}
TARGET_PART=${PART:-}
TARGET_TOPIC=${TOPIC:-}

root_dir=$(cd "$(dirname "$0")/.." && pwd)
export OUTPUT_ROOT VOICE

if ! command -v marp >/dev/null 2>&1; then
  echo "marp CLI is required to render slides" >&2
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required" >&2
  exit 1
fi
if ! command -v ffprobe >/dev/null 2>&1; then
  echo "ffprobe is required" >&2
  exit 1
fi

pushd "$root_dir" >/dev/null

go run ./cmd/render-slides

parts=($(find content -maxdepth 1 -mindepth 1 -type d | sort))
for part_dir in "${parts[@]}"; do
  part=$(basename "$part_dir")
  if [[ -n "$TARGET_PART" && "$part" != "$TARGET_PART" ]]; then
    continue
  fi
  topics=($(find "$part_dir" -maxdepth 1 -mindepth 1 -type d | sort))
  for topic_dir in "${topics[@]}"; do
    topic=$(basename "$topic_dir")
    if [[ -n "$TARGET_TOPIC" && "$topic" != "$TARGET_TOPIC" ]]; then
      continue
    fi
    slides="$topic_dir/slides.md"
    narratives="$topic_dir/narratives"
    if [[ -f "$slides" && -d "$narratives" ]]; then
      echo "\n=== Rendering $part/$topic ==="
      PART="$part" TOPIC="$topic" VOICE="$VOICE" OUTPUT_ROOT="$OUTPUT_ROOT" \
        "$root_dir/scripts/render_lesson.sh"
    fi
  done
done

popd >/dev/null
