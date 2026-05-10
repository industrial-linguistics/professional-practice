#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=${REPO_ROOT:-/home/professionalpractice/devel/professional-practice}
LOG_DIR=${AUDIO_WORKER_LOG_DIR:-$REPO_ROOT/logs/audio-generation}
LOCK_FILE=${AUDIO_WORKER_LOCK_FILE:-/home/professionalpractice/.cache/professional-practice-audio.lock}
MAX_TOPICS=${AUDIO_WORKER_MAX_TOPICS:-1}

mkdir -p "$LOG_DIR" "$(dirname "$LOCK_FILE")"
exec >> "$LOG_DIR/cron.log" 2>&1

echo "=== $(date -Is) audio generation cron start ==="

if [[ -f "$HOME/.profile" ]]; then
  # shellcheck disable=SC1090
  . "$HOME/.profile"
fi

if [[ -f "$HOME/.config/professional-practice.env" ]]; then
  # shellcheck disable=SC1090
  . "$HOME/.config/professional-practice.env"
fi

if [[ -z "${ELEVENLABS_API_KEY:-}" && -f "$HOME/.elevenlabs.io" ]]; then
  ELEVENLABS_API_KEY="$(tr -d '\r\n' < "$HOME/.elevenlabs.io")"
  export ELEVENLABS_API_KEY
fi

export PATH="$HOME/.local/node_modules/.bin:$HOME/.local/bin:$HOME/go/bin:/usr/local/go/bin:$PATH"

for required in git go python3 ffmpeg ffprobe marp flock; do
  if ! command -v "$required" >/dev/null 2>&1; then
    echo "missing required command: $required"
    exit 1
  fi
done

if [[ -z "${ELEVENLABS_API_KEY:-}" ]]; then
  echo "ELEVENLABS_API_KEY is not configured"
  exit 1
fi

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "another audio generation worker is already running"
  exit 0
fi

cd "$REPO_ROOT"
git pull --ff-only

python3 scripts/audio_generation_worker.py --max-topics "$MAX_TOPICS"

echo "=== $(date -Is) audio generation cron end ==="
