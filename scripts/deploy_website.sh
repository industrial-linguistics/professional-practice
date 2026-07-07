#!/bin/bash
set -euo pipefail

REMOTE_USER="${DEPLOYMENT_REMOTE_USER:-professionalpractice}"
REMOTE_HOST="${DEPLOYMENT_REMOTE_HOST:-merah.cassia.ifost.org.au}"
REMOTE_DIR="${DEPLOYMENT_REMOTE_DIR:-/var/www/vhosts/professional-practice.industrial-linguistics.com/htdocs}"
SOURCE_DIR="${DEPLOYMENT_SOURCE_DIR:-output/site}"
MIN_AUDIO_TOPICS="${DEPLOY_MIN_AUDIO_TOPICS:-5}"
SSH_KEY="${DEPLOYMENT_SSH_KEY:-}"

if [ ! -d "$SOURCE_DIR" ]; then
  echo "source directory not found: $SOURCE_DIR" >&2
  echo "run: python3 scripts/build_elearning.py" >&2
  exit 1
fi

if [ "$MIN_AUDIO_TOPICS" -gt 0 ]; then
  audio_count="$(find "$SOURCE_DIR/elearning/media" -path '*/audio.mp3' -type f 2>/dev/null | wc -l | tr -d ' ')"
  if [ "$audio_count" -lt "$MIN_AUDIO_TOPICS" ]; then
    echo "refusing to deploy: only $audio_count topic MP3 audio file(s) in $SOURCE_DIR; expected at least $MIN_AUDIO_TOPICS" >&2
    echo "sync generated media from raksasa or set DEPLOY_MIN_AUDIO_TOPICS=0 to override intentionally" >&2
    exit 1
  fi
fi

if [ -n "$SSH_KEY" ]; then
  RSYNC_SSH=(ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no)
else
  RSYNC_SSH=(ssh)
fi

rsync -avz -e "${RSYNC_SSH[*]}" "$SOURCE_DIR"/ "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"
"${RSYNC_SSH[@]}" "$REMOTE_USER@$REMOTE_HOST" \
  "rm -f '$REMOTE_DIR/textbook/main-amazon.pdf' '$REMOTE_DIR/elearning/textbook/main-amazon.pdf'"
