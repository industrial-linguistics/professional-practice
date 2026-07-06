#!/usr/bin/env bash
# Build the audio assets required by the e-learning course.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

CONTENT_DIR="${CONTENT_DIR:-content}"
FORCE_REBUILD="${FORCE_REBUILD:-false}"
SKIP_VALIDATION="${SKIP_VALIDATION:-false}"
SKIP_AUDIO="${SKIP_AUDIO:-false}"
AUDIO_TRANSCRIPT_VALIDATION="${AUDIO_TRANSCRIPT_VALIDATION:-false}"
ELEVENLABS_KEY_FILE="${ELEVENLABS_KEY_FILE:-$HOME/.elevenlabs.mq.io}"

usage() {
    echo "Usage: $0 [OPTIONS] [topic-path ...]"
    echo
    echo "Build e-learning audio from course content."
    echo
    echo "Options:"
    echo "  -f, --force        Force rebuild everything"
    echo "  -s, --skip-validation  Skip pre-generation validation"
    echo "  -a, --skip-audio   Skip audio generation and validate existing audio"
    echo "  --audio-transcript-validation  Run ASR transcript validation after audio generation"
    echo "  -h, --help         Show this help"
    exit 0
}

normalize_topic_path() {
    local path="$1"
    if [[ "$path" == "$PROJECT_ROOT"/content/* ]]; then
        printf 'content/%s\n' "${path#"$PROJECT_ROOT"/content/}"
    elif [[ "$path" == content/* ]]; then
        printf '%s\n' "$path"
    elif [[ "$path" == /* ]]; then
        printf '%s\n' "$path"
    else
        printf 'content/%s\n' "$path"
    fi
}

TOPICS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--force)
            FORCE_REBUILD=true
            shift
            ;;
        -s|--skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        -a|--skip-audio)
            SKIP_AUDIO=true
            shift
            ;;
        --audio-transcript-validation)
            AUDIO_TRANSCRIPT_VALIDATION=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            TOPICS+=("$1")
            shift
            ;;
    esac
done

cd "$PROJECT_ROOT"

if [[ "$SKIP_AUDIO" != "true" && -z "${ELEVENLABS_API_KEY:-}" ]]; then
    if [[ -f "$ELEVENLABS_KEY_FILE" ]]; then
        ELEVENLABS_API_KEY="$(tr -d '\r\n' < "$ELEVENLABS_KEY_FILE")"
        export ELEVENLABS_API_KEY
    else
        echo "Warning: ELEVENLABS_API_KEY not set. Set SKIP_AUDIO=true to validate existing audio only." >&2
    fi
fi

echo "Professional Practice audio build pipeline"
echo

if [[ "$FORCE_REBUILD" == "true" ]]; then
    echo "Force rebuild enabled - clearing manifest"
    python3 scripts/build_manifest.py reset
fi

if [[ ${#TOPICS[@]} -eq 0 ]]; then
    echo "Checking what needs audio..."
    mapfile -t TOPICS < <(
        CONTENT_DIR="$CONTENT_DIR" python3 - <<'PY'
import os
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from build_manifest import BuildManifest  # noqa: E402

manifest = BuildManifest()
for topic_path, _reason in manifest.get_topics_to_build(Path(os.environ["CONTENT_DIR"])):
    print(topic_path)
PY
    )

    if [[ ${#TOPICS[@]} -eq 0 ]]; then
        echo "Everything is up to date."
        exit 0
    fi

    echo "Building ${#TOPICS[@]} topic(s)."
fi

echo
echo "Building Go audio tools..."
go build -o bin/vtt-generator ./cmd/vtt-generator
go build -o bin/voicer ./cmd/voicer

BUILD_RESULTS=()
FAILED_TOPICS=()

for TOPIC_PATH in "${TOPICS[@]}"; do
    TOPIC_PATH="$(normalize_topic_path "$TOPIC_PATH")"

    TOPIC_NAME="$(basename "$TOPIC_PATH")"
    PART_NAME="$(basename "$(dirname "$TOPIC_PATH")")"

    echo
    echo "Building audio: $PART_NAME / $TOPIC_NAME"

    if [[ "$SKIP_VALIDATION" != "true" ]]; then
        echo "[1/4] Pre-generation validation..."
        if ! python3 scripts/validate_content.py "$TOPIC_PATH"; then
            echo "Validation failed for $TOPIC_PATH" >&2
            FAILED_TOPICS+=("$TOPIC_PATH")
            python3 scripts/build_manifest.py mark-failed "$TOPIC_PATH" "Pre-generation validation failed"
            continue
        fi
    fi

    echo "[2/4] Generating subtitles..."
    if ! ./bin/vtt-generator "$TOPIC_PATH"; then
        echo "VTT generation failed for $TOPIC_PATH" >&2
        FAILED_TOPICS+=("$TOPIC_PATH")
        continue
    fi

    if [[ "$SKIP_AUDIO" != "true" ]]; then
        echo "[3/4] Generating audio..."
        VOICER_ARGS=(
            -v "$TOPIC_PATH/subtitles.vtt"
            -o "$TOPIC_PATH/audio.wav"
            --autopad
        )
        if [[ -n "${VOICER_TEMP_DIR:-}" ]]; then
            VOICER_ARGS+=(--temp-dir "$VOICER_TEMP_DIR")
        fi
        if ! ./bin/voicer "${VOICER_ARGS[@]}"; then
            echo "Audio generation failed for $TOPIC_PATH" >&2
            FAILED_TOPICS+=("$TOPIC_PATH")
            continue
        fi
    else
        echo "[3/4] Skipping audio generation"
    fi

    echo "[4/4] Validating audio outputs..."
    if ! python3 scripts/validate_outputs.py --audio-only "$TOPIC_PATH"; then
        echo "Audio output validation failed for $TOPIC_PATH" >&2
        FAILED_TOPICS+=("$TOPIC_PATH")
        continue
    fi

    if [[ "$AUDIO_TRANSCRIPT_VALIDATION" == "true" ]]; then
        echo "[extra] Validating audio transcript..."
        if ! python3 scripts/validate_audio_transcript.py "$TOPIC_PATH"; then
            echo "Audio transcript validation failed for $TOPIC_PATH" >&2
            FAILED_TOPICS+=("$TOPIC_PATH")
            continue
        fi
    fi

    python3 scripts/build_manifest.py update "$TOPIC_PATH"
    BUILD_RESULTS+=("$TOPIC_PATH")
    echo "Built audio for $PART_NAME/$TOPIC_NAME"
done

echo
echo "Build summary"
echo "============="

if [[ ${#BUILD_RESULTS[@]} -gt 0 ]]; then
    echo "Successfully built:"
    for result in "${BUILD_RESULTS[@]}"; do
        echo "  $result"
    done
fi

if [[ ${#FAILED_TOPICS[@]} -gt 0 ]]; then
    echo "Failed to build:" >&2
    for topic in "${FAILED_TOPICS[@]}"; do
        echo "  $topic" >&2
    done
    exit 1
fi

python3 scripts/build_manifest.py status
