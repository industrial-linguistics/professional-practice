# Video Rendering Pipeline

This document describes the automated video rendering pipeline that converts course content (slides and narratives) into finished video lessons.

## Overview

The pipeline consists of six stages:

1. **Pre-generation Validation** - Verify content structure and quality
2. **VTT Generation** - Convert narratives to WebVTT subtitles with timing
3. **Slide Rendering** - Convert Marp markdown to PNG images
4. **Audio Generation** - Generate narration using ElevenLabs TTS
5. **Video Assembly** - Combine slides and audio into final video
6. **Post-generation Validation** - Verify outputs are correct

## Quick Start

### Setup

```bash
# Install dependencies
./envsetup.sh

# Configure ElevenLabs API key (required for audio)
echo "your_api_key_here" > ~/.elevenlabs.io
```

### Build Videos

```bash
# Build only what has changed (incremental)
./scripts/build_videos.sh

# Force rebuild everything
./scripts/build_videos.sh --force

# Build specific topic
./scripts/build_videos.sh content/part-01/overview

# Skip audio generation (use existing audio files)
./scripts/build_videos.sh --skip-audio
```

## Pipeline Components

### 1. VTT Generator (`cmd/vtt-generator`)

Converts narrative markdown files into WebVTT subtitle files with proper timing.

**Features:**
- Counts words to estimate speech duration (default: 150 words/minute)
- Validates narrative count matches slide count
- Generates properly formatted WebVTT files

**Usage:**
```bash
bin/vtt-generator content/part-01/overview
```

**Input:** `content/part-01/overview/narratives/*.md`
**Output:** `content/part-01/overview/subtitles.vtt`

### 2. Slide Renderer (`cmd/render-slides`)

Renders Marp markdown slides to PNG images.

**Usage:**
```bash
bin/render-slides
```

**Input:** `content/**/slides.md`
**Output:** `assets/slide-images/part-XX/topic-name/slide.001.png`, etc.

### 3. Audio Generator (`cmd/voicer`)

Generates audio narration using ElevenLabs text-to-speech API.

**Features:**
- S3 caching with MD5 checksums (avoids regenerating unchanged audio)
- Context-aware speech (uses previous/next text for natural flow)
- Automatic padding calculation
- Speed adjustment for timing alignment
- Collision detection and resolution

**Usage:**
```bash
bin/voicer \
  -v content/part-01/overview/subtitles.vtt \
  -o content/part-01/overview/audio.wav \
  --autopad
```

**Environment Variables:**
- `ELEVENLABS_API_KEY` - API key for ElevenLabs
- `VOICER_S3_BUCKET` - S3 bucket for audio caching (optional)

### 4. Video Assembler (`scripts/assemble_video.sh`)

Combines slide images and audio into final MP4 video.

**Process:**
1. Parse VTT file to extract timing information
2. Create ffmpeg concat file with durations
3. Generate silent video from slides (1920x1080, 30fps)
4. Merge audio with video
5. Validate output properties

**Usage:**
```bash
./scripts/assemble_video.sh content/part-01/overview
```

**Input:**
- `assets/slide-images/part-01/overview/slide.*.png`
- `content/part-01/overview/subtitles.vtt`
- `content/part-01/overview/audio.wav`

**Output:** `content/part-01/overview/final.mp4`

## Validation Layers

### Level 1: Pre-Generation Validation (`scripts/validate_content.py`)

Fast checks before any generation:

- ✓ Required files exist (slides.md, narratives/)
- ✓ Slide count matches narrative count
- ✓ Markdown syntax is valid
- ✓ Word counts are reasonable (50-250 words)
- ✓ No broken links or unclosed code blocks

### Level 2: Post-Generation Validation (`scripts/validate_outputs.py`)

Fast checks after generation:

- ✓ VTT file is valid WebVTT format
- ✓ All slide images exist and are valid PNG
- ✓ Resolution is correct (1920x1080)
- ✓ Audio file exists and has duration > 0
- ✓ Video file exists with correct codecs (h264/aac)
- ✓ A/V sync is within 500ms

### Level 3: Audio Quality Validation (Optional)

Requires Whisper for transcription:

- Transcribe audio and calculate Word Error Rate (WER)
- Check for audio clipping or excessive silence
- Verify segment timing alignment

### Level 4: A/V Sync Validation (Future)

- Detect scene changes in video
- Verify slide transitions align with VTT timestamps
- Check for frame corruption

## Incremental Build System

The build manifest system (`scripts/build_manifest.py`) tracks file hashes and only rebuilds what changed.

**Commands:**
```bash
# Check what needs to be built
python3 scripts/build_manifest.py check content

# Update manifest after successful build
python3 scripts/build_manifest.py update content/part-01/overview

# Show build status
python3 scripts/build_manifest.py status

# Clear manifest (rebuild everything)
python3 scripts/build_manifest.py reset
```

**Manifest Location:** `.build-manifest.json`

**What triggers rebuild:**
- Source file changed (slides.md, narratives/*.md, images/*)
- Output file missing (subtitles.vtt, audio.wav, final.mp4)
- Never built before

## GitHub Actions Integration

The pipeline runs automatically on push via `.github/workflows/video-pipeline.yml`.

**Triggers:**
- Push to main branch with changes to content files
- Manual workflow dispatch (with force rebuild option)

**Secrets Required:**
- `ELEVENLABS_API_KEY` - For audio generation
- `VOICER_S3_BUCKET` - For audio caching (optional)
- `AWS_ACCESS_KEY_ID` - For S3 access (optional)
- `AWS_SECRET_ACCESS_KEY` - For S3 access (optional)

**Artifacts:**
- `videos/` - All generated final.mp4 files
- `build-manifest` - Updated build tracking
- `test-report` - Validation results

## Cost Optimization

### S3 Audio Caching

Enable S3 caching to avoid regenerating unchanged audio:

```bash
export VOICER_S3_BUCKET=my-bucket-name
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
```

Audio segments are cached by MD5 hash of: (text, context, voice_id, speed)

**Cost savings:**
- Unchanged narratives: 100% savings (cached)
- Changed narratives: Only regenerate changed segments
- Typical rebuild: 10-20% of full generation cost

### Incremental Builds

The build manifest system ensures we only rebuild topics where content changed.

**Typical scenarios:**
- Fix typo in one narrative: Rebuild 1 topic (~1-2 minutes)
- Add new topic: Build only that topic
- Update all Part 1: Build only Part 1 topics
- Fresh clone: Build everything (~10-30 minutes for full course)

## Troubleshooting

### "Validation failed: X slides but Y narratives"

The number of slides in `slides.md` doesn't match narrative files.

**Fix:** Ensure each slide has a corresponding narrative file, or vice versa.

### "Segment X exceeds output duration"

Audio segment is too long for the allocated time in VTT.

**Fix:** The voicer tool has `--autospeed` to automatically speed up long segments, or use `--autopad` to add padding.

### "Video and audio duration differ by Xs"

A/V sync issue - usually means padding is insufficient.

**Fix:** Use `--autopad` flag with voicer, or increase `--padding` manually.

### "ELEVENLABS_API_KEY not set"

API key is required for audio generation.

**Fix:**
```bash
echo "your_api_key_here" > ~/.elevenlabs.io
```

Or use `--skip-audio` to skip audio generation (for testing).

### Build hangs during audio generation

ElevenLabs API may be slow or rate-limited.

**Fix:**
- Check API status at status.elevenlabs.io
- Use S3 caching to reduce API calls
- Reduce concurrent builds

## Architecture Decisions

### Why Go for generators?

- Fast compilation and execution
- Easy cross-platform distribution
- Good markdown parsing libraries
- Existing voicer tool in Go

### Why Python for validation?

- Rich ecosystem for media analysis (ffprobe wrappers)
- Easy JSON/text processing
- Optional Whisper integration for transcription

### Why bash for assembly?

- Direct ffmpeg integration
- Simple scripting for pipeline steps
- Easy debugging and iteration

### Why VTT for timing?

- Industry standard subtitle format
- Human-readable and editable
- Well-supported by video players
- Easy to parse and generate

## Performance

### Typical Build Times

**Single topic (incremental):**
- Validation: < 1s
- VTT generation: < 1s
- Slide rendering: 2-5s
- Audio generation: 10-30s (or instant if cached)
- Video assembly: 5-10s
- **Total: ~20-50s** (or ~10s with cached audio)

**Full course (8 parts, ~50 topics):**
- First build: 20-40 minutes
- Incremental: 1-5 minutes (typical changes)
- Force rebuild (with S3 cache): 10-15 minutes

### Optimization Tips

1. **Use S3 caching** - Biggest impact on rebuild times
2. **Use incremental builds** - Only build what changed
3. **Skip validation** - Use `--skip-validation` for iteration
4. **Parallel builds** - Run multiple topics in parallel (future)

## Future Enhancements

- [ ] SCORM packaging for LMS integration
- [ ] E-book generation (PDF/EPUB)
- [ ] Whisper-based quality validation
- [ ] Parallel topic builds
- [ ] Video hosting integration (YouTube, Vimeo)
- [ ] Chapter markers in video
- [ ] Closed captions support
- [ ] Multi-language support
- [ ] Advanced scene transitions
- [ ] Background music support
