#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=${REPO_ROOT:-/home/professionalpractice/devel/professional-practice}
LOG_DIR=${AUDIO_WORKER_LOG_DIR:-$REPO_ROOT/logs/audio-generation}
LOCK_FILE=${AUDIO_WORKER_LOCK_FILE:-/home/professionalpractice/.cache/professional-practice-audio.lock}
MAX_TOPICS=${AUDIO_WORKER_MAX_TOPICS:-1}
VOICER_TEMP_DIR=${AUDIO_WORKER_VOICER_TEMP_DIR:-/home/professionalpractice/.cache/professional-practice-audio-tmp/voicer-audio}
ELEVENLABS_KEY_FILE=${ELEVENLABS_KEY_FILE:-$HOME/.elevenlabs.mq.io}
STATE_FILE=${AUDIO_WORKER_STATE_FILE:-state/audio-worker-state.json}
export VOICER_TEMP_DIR

mkdir -p "$LOG_DIR" "$(dirname "$LOCK_FILE")" "$VOICER_TEMP_DIR"
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

if [[ -z "${ELEVENLABS_API_KEY:-}" && -f "$ELEVENLABS_KEY_FILE" ]]; then
  ELEVENLABS_API_KEY="$(tr -d '\r\n' < "$ELEVENLABS_KEY_FILE")"
  export ELEVENLABS_API_KEY
fi

export PATH="$HOME/.local/node_modules/.bin:$HOME/.local/bin:$HOME/go/bin:/usr/local/go/bin:$PATH"

for required in git go python3 ffmpeg ffprobe flock; do
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

python3 scripts/audio_generation_worker.py --max-topics "$MAX_TOPICS" --state-file "$STATE_FILE"

if [[ "${AUDIO_WORKER_PUBLISH_SITE:-true}" == "true" ]]; then
  if python3 - "$STATE_FILE" <<'PY'
import json
import sys
from pathlib import Path

state_path = Path(sys.argv[1])
if not state_path.exists():
    raise SystemExit(1)
state = json.loads(state_path.read_text())
runs = state.get("runs") or []
if not runs:
    raise SystemExit(1)
last_run = runs[-1]
for result in last_run.get("results", []):
    if result.get("status") == "built":
        raise SystemExit(0)
raise SystemExit(1)
PY
  then
    echo "New audio built; rebuilding and publishing e-learning site"
    python3 scripts/build_elearning.py
    scripts/deploy_website.sh
  else
    echo "No new audio built; skipping site publish"
  fi
fi

echo "=== $(date -Is) audio generation cron end ==="
