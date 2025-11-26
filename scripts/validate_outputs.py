#!/usr/bin/env python3
"""
Post-generation output validation
Level 2: Fast validation that outputs were created correctly
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import json

class ValidationResult:
    def __init__(self, passed: bool, message: str = "", details: Dict = None):
        self.passed = passed
        self.message = message
        self.details = details or {}

    def __bool__(self):
        return self.passed

def check_file_exists(file_path: Path, description: str) -> ValidationResult:
    """Check if a file exists"""
    if not file_path.exists():
        return ValidationResult(False, f"{description} not found: {file_path}")
    return ValidationResult(True, f"✓ {description} found")

def validate_vtt_file(vtt_file: Path) -> ValidationResult:
    """Validate VTT file format"""
    try:
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for VTT header
        if not content.startswith('WEBVTT'):
            return ValidationResult(False, "VTT file missing WEBVTT header")

        # Count entries
        entry_count = content.count('-->')

        if entry_count == 0:
            return ValidationResult(False, "VTT file has no subtitle entries")

        return ValidationResult(True, f"✓ Valid VTT with {entry_count} entries")

    except Exception as e:
        return ValidationResult(False, f"Failed to validate VTT: {e}")

def validate_image(image_path: Path) -> Tuple[bool, int, int]:
    """Validate PNG image and get dimensions"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=width,height',
             '-of', 'json', str(image_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return False, 0, 0

        data = json.loads(result.stdout)
        stream = data['streams'][0]
        width = stream['width']
        height = stream['height']

        return True, width, height

    except Exception:
        return False, 0, 0

def get_media_duration(file_path: Path) -> float:
    """Get duration of media file in seconds"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return -1

        return float(result.stdout.strip())

    except Exception:
        return -1

def get_codec_info(file_path: Path) -> Tuple[str, str]:
    """Get video and audio codec information"""
    try:
        # Get video codec
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=codec_name',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)],
            capture_output=True,
            text=True
        )
        video_codec = result.stdout.strip() if result.returncode == 0 else "unknown"

        # Get audio codec
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
             '-show_entries', 'stream=codec_name',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)],
            capture_output=True,
            text=True
        )
        audio_codec = result.stdout.strip() if result.returncode == 0 else "unknown"

        return video_codec, audio_codec

    except Exception:
        return "unknown", "unknown"

def validate_topic_outputs(topic_path: Path) -> ValidationResult:
    """Validate all outputs for a topic"""
    errors = []
    warnings = []
    details = {}

    # Get part and topic names
    topic_name = topic_path.name
    part_name = topic_path.parent.name

    # Check VTT file
    vtt_file = topic_path / "subtitles.vtt"
    result = check_file_exists(vtt_file, "VTT file")
    if not result:
        errors.append(result.message)
    else:
        result = validate_vtt_file(vtt_file)
        if not result:
            errors.append(result.message)
        else:
            details['vtt'] = result.message

    # Check slide images
    slides_dir = Path("assets/slide-images") / part_name / topic_name
    if not slides_dir.exists():
        errors.append(f"Slide images directory not found: {slides_dir}")
    else:
        image_files = sorted(slides_dir.glob("slide.*.png"))
        if len(image_files) == 0:
            errors.append(f"No slide images found in {slides_dir}")
        else:
            # Validate first image
            valid, width, height = validate_image(image_files[0])
            if not valid:
                errors.append(f"Invalid image: {image_files[0]}")
            else:
                details['slides'] = f"✓ {len(image_files)} slides ({width}x{height})"

                # Check resolution
                if (width, height) not in [(1920, 1080), (1280, 720)]:
                    warnings.append(f"Unusual resolution: {width}x{height}")

    # Check audio file
    audio_file = topic_path / "audio.wav"
    result = check_file_exists(audio_file, "Audio file")
    if not result:
        errors.append(result.message)
    else:
        duration = get_media_duration(audio_file)
        if duration < 0:
            errors.append("Failed to get audio duration")
        elif duration == 0:
            errors.append("Audio file has zero duration")
        else:
            details['audio'] = f"✓ Audio file ({duration:.1f}s)"

    # Check video file
    video_file = topic_path / "final.mp4"
    result = check_file_exists(video_file, "Video file")
    if not result:
        errors.append(result.message)
    else:
        duration = get_media_duration(video_file)
        if duration < 0:
            errors.append("Failed to get video duration")
        elif duration == 0:
            errors.append("Video file has zero duration")
        else:
            video_codec, audio_codec = get_codec_info(video_file)
            details['video'] = f"✓ Video file ({duration:.1f}s, {video_codec}/{audio_codec})"

            # Validate codecs
            if video_codec != "h264":
                warnings.append(f"Unexpected video codec: {video_codec} (expected h264)")
            if audio_codec not in ["aac", "mp3"]:
                warnings.append(f"Unexpected audio codec: {audio_codec}")

    # Check A/V sync if both exist
    if 'audio' in details and 'video' in details:
        audio_duration = get_media_duration(audio_file)
        video_duration = get_media_duration(video_file)

        if audio_duration > 0 and video_duration > 0:
            duration_diff = abs(audio_duration - video_duration)
            if duration_diff > 0.5:
                warnings.append(f"A/V duration mismatch: {duration_diff:.2f}s")
            else:
                details['sync'] = f"✓ A/V sync within {duration_diff:.2f}s"

    # Compile result
    if errors:
        return ValidationResult(False, f"{len(errors)} error(s): {'; '.join(errors)}", details)

    message = f"✓ All outputs validated"
    if warnings:
        message += f" ({len(warnings)} warning(s))"

    return ValidationResult(True, message, {**details, 'warnings': warnings})

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_outputs.py <topic-path> [<topic-path> ...]")
        print("Example: validate_outputs.py content/part-01/overview")
        sys.exit(1)

    topic_paths = [Path(p) for p in sys.argv[1:]]

    # Print results
    print("\n" + "=" * 70)
    print("OUTPUT VALIDATION RESULTS")
    print("=" * 70)

    all_passed = True
    total_warnings = 0

    for topic_path in topic_paths:
        if not topic_path.exists():
            print(f"\n❌ FAIL {topic_path}")
            print(f"  Path not found")
            all_passed = False
            continue

        result = validate_topic_outputs(topic_path)
        status = "✅ PASS" if result.passed else "❌ FAIL"

        print(f"\n{status} {topic_path}")
        print(f"  {result.message}")

        if result.details:
            for key, value in result.details.items():
                if key != 'warnings':
                    print(f"  {value}")

        if 'warnings' in result.details:
            for warning in result.details['warnings']:
                print(f"  ⚠️  {warning}")
                total_warnings += 1

        if not result.passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print(f"✅ All outputs validated")
        if total_warnings > 0:
            print(f"⚠️  {total_warnings} warning(s) found")
    else:
        print("❌ Output validation failed")
    print("=" * 70 + "\n")

    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()
