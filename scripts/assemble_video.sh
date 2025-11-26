#!/bin/bash
# Assemble video from slide images and audio
# Usage: ./assemble_video.sh <topic-path>

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <topic-path>"
    echo "Example: $0 content/part-01/overview"
    exit 1
fi

TOPIC_PATH="$1"
TOPIC_NAME=$(basename "$TOPIC_PATH")
PART_NAME=$(basename "$(dirname "$TOPIC_PATH")")

# Find the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Paths
SLIDES_DIR="$PROJECT_ROOT/assets/slide-images/$PART_NAME/$TOPIC_NAME"
VTT_FILE="$TOPIC_PATH/subtitles.vtt"
AUDIO_FILE="$TOPIC_PATH/audio.wav"
OUTPUT_DIR="$TOPIC_PATH"
TEMP_DIR="$OUTPUT_DIR/temp"

# Validate inputs
if [ ! -d "$SLIDES_DIR" ]; then
    echo "Error: Slides directory not found: $SLIDES_DIR"
    echo "Run 'go run cmd/render-slides' first"
    exit 1
fi

if [ ! -f "$VTT_FILE" ]; then
    echo "Error: VTT file not found: $VTT_FILE"
    echo "Run 'vtt-generator $TOPIC_PATH' first"
    exit 1
fi

if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: Audio file not found: $AUDIO_FILE"
    echo "Run 'voicer' to generate audio first"
    exit 1
fi

# Create temp directory
mkdir -p "$TEMP_DIR"

echo "Assembling video for $PART_NAME/$TOPIC_NAME..."

# Step 1: Parse VTT to create timing file
echo "Creating timing file from VTT..."
python3 - <<'PYTHON_SCRIPT' "$VTT_FILE" "$TEMP_DIR/timings.txt"
import sys
import re

vtt_file = sys.argv[1]
output_file = sys.argv[2]

with open(vtt_file, 'r') as f:
    content = f.read()

# Parse VTT entries
entries = []
pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})'

for match in re.finditer(pattern, content):
    index = int(match.group(1))
    start = match.group(2)
    end = match.group(3)

    # Convert timestamp to seconds
    def to_seconds(ts):
        h, m, s = ts.split(':')
        s, ms = s.split('.')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

    start_sec = to_seconds(start)
    end_sec = to_seconds(end)
    duration = end_sec - start_sec

    entries.append((index, duration))

# Write timing information
with open(output_file, 'w') as f:
    for index, duration in entries:
        f.write(f"{index}\t{duration:.3f}\n")

print(f"Parsed {len(entries)} timing entries")
PYTHON_SCRIPT

# Step 2: Create ffmpeg concat file
echo "Creating ffmpeg concat file..."
CONCAT_FILE="$TEMP_DIR/concat.txt"
> "$CONCAT_FILE"

while IFS=$'\t' read -r index duration; do
    slide_file="$SLIDES_DIR/slide.$(printf '%03d' "$index").png"

    if [ ! -f "$slide_file" ]; then
        echo "Error: Slide image not found: $slide_file"
        exit 1
    fi

    echo "file '$slide_file'" >> "$CONCAT_FILE"
    echo "duration $duration" >> "$CONCAT_FILE"
done < "$TEMP_DIR/timings.txt"

# Add the last slide one more time (ffmpeg concat requirement)
last_index=$(tail -n 1 "$TEMP_DIR/timings.txt" | cut -f1)
last_slide="$SLIDES_DIR/slide.$(printf '%03d' "$last_index").png"
echo "file '$last_slide'" >> "$CONCAT_FILE"

echo "Created concat file with $(wc -l < "$CONCAT_FILE") entries"

# Step 3: Create silent video from slides
echo "Creating silent video from slides..."
SILENT_VIDEO="$TEMP_DIR/silent.mp4"

ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black" \
    -r 30 -pix_fmt yuv420p \
    -c:v libx264 -preset fast -crf 23 \
    "$SILENT_VIDEO" 2>&1 | grep -v "deprecated pixel format"

if [ ! -f "$SILENT_VIDEO" ]; then
    echo "Error: Failed to create silent video"
    exit 1
fi

echo "Silent video created: $SILENT_VIDEO"

# Step 4: Get durations for validation
VIDEO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$SILENT_VIDEO")
AUDIO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE")

echo "Video duration: ${VIDEO_DURATION}s"
echo "Audio duration: ${AUDIO_DURATION}s"

# Check duration mismatch
DURATION_DIFF=$(python3 -c "print(abs($VIDEO_DURATION - $AUDIO_DURATION))")
if (( $(echo "$DURATION_DIFF > 1.0" | bc -l) )); then
    echo "Warning: Video and audio duration differ by ${DURATION_DIFF}s"
    echo "This may indicate a problem with timing"
fi

# Step 5: Merge audio and video
echo "Merging audio and video..."
FINAL_VIDEO="$OUTPUT_DIR/final.mp4"

ffmpeg -y -i "$SILENT_VIDEO" -i "$AUDIO_FILE" \
    -c:v copy -c:a aac -b:a 192k \
    -shortest \
    "$FINAL_VIDEO" 2>&1 | grep -v "deprecated pixel format"

if [ ! -f "$FINAL_VIDEO" ]; then
    echo "Error: Failed to create final video"
    exit 1
fi

# Step 6: Validate output
FINAL_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$FINAL_VIDEO")
echo "Final video duration: ${FINAL_DURATION}s"

# Check video properties
VIDEO_CODEC=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$FINAL_VIDEO")
AUDIO_CODEC=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$FINAL_VIDEO")
VIDEO_WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 "$FINAL_VIDEO")
VIDEO_HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 "$FINAL_VIDEO")

echo "Video codec: $VIDEO_CODEC"
echo "Audio codec: $AUDIO_CODEC"
echo "Resolution: ${VIDEO_WIDTH}x${VIDEO_HEIGHT}"

# Clean up temp files
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Video assembly complete: $FINAL_VIDEO"
echo ""
