#!/bin/bash
# Master build script for video pipeline
# Handles the full workflow: validate -> generate -> assemble -> test

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONTENT_DIR="${CONTENT_DIR:-$PROJECT_ROOT/content}"
FORCE_REBUILD="${FORCE_REBUILD:-false}"
SKIP_VALIDATION="${SKIP_VALIDATION:-false}"
SKIP_AUDIO="${SKIP_AUDIO:-false}"

# Check if ELEVENLABS_API_KEY is set
if [ "$SKIP_AUDIO" != "true" ] && [ -z "$ELEVENLABS_API_KEY" ]; then
    if [ -f "$HOME/.elevenlabs.io" ]; then
        export ELEVENLABS_API_KEY=$(cat "$HOME/.elevenlabs.io")
    else
        echo -e "${YELLOW}Warning: ELEVENLABS_API_KEY not set. Set SKIP_AUDIO=true to skip audio generation.${NC}"
    fi
fi

usage() {
    echo "Usage: $0 [OPTIONS] [topic-path ...]"
    echo ""
    echo "Build videos from course content"
    echo ""
    echo "Options:"
    echo "  -f, --force        Force rebuild everything"
    echo "  -s, --skip-validation  Skip pre-generation validation"
    echo "  -a, --skip-audio   Skip audio generation (use existing)"
    echo "  -h, --help         Show this help"
    echo ""
    echo "Examples:"
    echo "  $0                              # Build only what changed"
    echo "  $0 -f                           # Force rebuild everything"
    echo "  $0 content/part-01/overview     # Build specific topic"
    exit 0
}

# Parse arguments
TOPICS=()
while [[ $# -gt 0 ]]; do
    case $1 in
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

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          Professional Practice Video Build Pipeline         ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Determine what to build
if [ "$FORCE_REBUILD" = "true" ]; then
    echo -e "${YELLOW}Force rebuild enabled - clearing manifest${NC}"
    python3 scripts/build_manifest.py reset
fi

if [ ${#TOPICS[@]} -eq 0 ]; then
    echo "Checking what needs to be built..."
    python3 scripts/build_manifest.py check "$CONTENT_DIR" | tee /tmp/build_check.txt

    # Parse topics from build check output
    mapfile -t TOPICS < <(grep "📹" /tmp/build_check.txt | sed 's/.*📹 //' || true)

    if [ ${#TOPICS[@]} -eq 0 ]; then
        echo -e "${GREEN}✅ Everything is up to date!${NC}"
        exit 0
    fi

    echo ""
    echo -e "${BLUE}Building ${#TOPICS[@]} topic(s)${NC}"
fi

# Build Go tools
echo ""
echo -e "${BLUE}Building Go tools...${NC}"
go build -o bin/vtt-generator ./cmd/vtt-generator
go build -o bin/render-slides ./cmd/render-slides
go build -o bin/voicer ./cmd/voicer

# Track results
BUILD_RESULTS=()
FAILED_TOPICS=()

# Process each topic
for TOPIC_PATH in "${TOPICS[@]}"; do
    TOPIC_PATH="${TOPIC_PATH#content/}"  # Remove content/ prefix if present
    TOPIC_PATH="content/$TOPIC_PATH"

    TOPIC_NAME=$(basename "$TOPIC_PATH")
    PART_NAME=$(basename "$(dirname "$TOPIC_PATH")")

    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Building: $PART_NAME / $TOPIC_NAME${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"

    # Step 1: Pre-generation validation
    if [ "$SKIP_VALIDATION" != "true" ]; then
        echo ""
        echo -e "${YELLOW}[1/6] Pre-generation validation...${NC}"
        if ! python3 scripts/validate_content.py "$TOPIC_PATH"; then
            echo -e "${RED}❌ Validation failed for $TOPIC_PATH${NC}"
            FAILED_TOPICS+=("$TOPIC_PATH")
            python3 scripts/build_manifest.py mark-failed "$TOPIC_PATH" "Pre-generation validation failed"
            continue
        fi
    fi

    # Step 2: Generate VTT
    echo ""
    echo -e "${YELLOW}[2/6] Generating subtitles (VTT)...${NC}"
    if ! ./bin/vtt-generator "$TOPIC_PATH"; then
        echo -e "${RED}❌ VTT generation failed${NC}"
        FAILED_TOPICS+=("$TOPIC_PATH")
        continue
    fi

    # Step 3: Render slides
    echo ""
    echo -e "${YELLOW}[3/6] Rendering slides to PNG...${NC}"
    if ! ./bin/render-slides; then
        echo -e "${RED}❌ Slide rendering failed${NC}"
        FAILED_TOPICS+=("$TOPIC_PATH")
        continue
    fi

    # Step 4: Generate audio
    if [ "$SKIP_AUDIO" != "true" ]; then
        echo ""
        echo -e "${YELLOW}[4/6] Generating audio with ElevenLabs...${NC}"
        if ! ./bin/voicer \
            -v "$TOPIC_PATH/subtitles.vtt" \
            -o "$TOPIC_PATH/audio.wav" \
            --autopad; then
            echo -e "${RED}❌ Audio generation failed${NC}"
            FAILED_TOPICS+=("$TOPIC_PATH")
            continue
        fi
    else
        echo -e "${YELLOW}[4/6] Skipping audio generation${NC}"
    fi

    # Step 5: Assemble video
    echo ""
    echo -e "${YELLOW}[5/6] Assembling video...${NC}"
    if ! bash scripts/assemble_video.sh "$TOPIC_PATH"; then
        echo -e "${RED}❌ Video assembly failed${NC}"
        FAILED_TOPICS+=("$TOPIC_PATH")
        continue
    fi

    # Step 6: Validate outputs
    echo ""
    echo -e "${YELLOW}[6/6] Validating outputs...${NC}"
    if ! python3 scripts/validate_outputs.py "$TOPIC_PATH"; then
        echo -e "${RED}❌ Output validation failed${NC}"
        FAILED_TOPICS+=("$TOPIC_PATH")
        continue
    fi

    # Update manifest
    python3 scripts/build_manifest.py update "$TOPIC_PATH"

    BUILD_RESULTS+=("✅ $TOPIC_PATH")
    echo ""
    echo -e "${GREEN}✅ Successfully built $PART_NAME/$TOPIC_NAME${NC}"
done

# Print summary
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                      BUILD SUMMARY                           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ ${#BUILD_RESULTS[@]} -gt 0 ]; then
    echo -e "${GREEN}Successfully built:${NC}"
    for result in "${BUILD_RESULTS[@]}"; do
        echo "  $result"
    done
    echo ""
fi

if [ ${#FAILED_TOPICS[@]} -gt 0 ]; then
    echo -e "${RED}Failed to build:${NC}"
    for topic in "${FAILED_TOPICS[@]}"; do
        echo "  ❌ $topic"
    done
    echo ""
    exit 1
fi

echo -e "${GREEN}🎉 All builds completed successfully!${NC}"
echo ""

# Show build status
python3 scripts/build_manifest.py status
