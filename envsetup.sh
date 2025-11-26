#!/bin/bash
set -e

# Add Revoicer package repository
echo "deb [trusted=yes] https://packages.industrial-linguistics.com/revoicer/debian stable main" | sudo tee /etc/apt/sources.list.d/revoicer.list >/dev/null

# Install base tools
sudo apt-get update
sudo apt-get install -y \
    nodejs \
    npm \
    ffmpeg \
    golang-go \
    jq \
    revoicer \
    python3 \
    python3-pip \
    bc \
    fonts-dejavu-core

# Install Marp CLI for slide rendering
sudo npm install -g @marp-team/marp-cli

# Install Python dependencies (optional - for audio quality testing)
# Uncomment to enable Whisper-based audio validation
# pip3 install openai-whisper jiwer

# Build Go tools
echo "Building Go tools..."
mkdir -p bin
go build -o bin/vtt-generator ./cmd/vtt-generator
go build -o bin/render-slides ./cmd/render-slides
go build -o bin/voicer ./cmd/voicer
go build -o bin/run_sheets ./cmd/run_sheets

echo ""
echo "Environment setup complete!"
echo ""
echo "Available commands:"
echo "  bin/vtt-generator   - Generate VTT subtitles from narratives"
echo "  bin/render-slides   - Render Marp slides to PNG"
echo "  bin/voicer          - Generate audio using ElevenLabs"
echo "  bin/run_sheets      - Generate instructor PDF run sheets"
echo ""
echo "Scripts:"
echo "  scripts/build_videos.sh       - Build videos (full pipeline)"
echo "  scripts/assemble_video.sh     - Assemble single video from components"
echo "  scripts/validate_content.py   - Validate content before building"
echo "  scripts/validate_outputs.py   - Validate generated outputs"
echo "  scripts/build_manifest.py     - Manage incremental builds"
echo ""
