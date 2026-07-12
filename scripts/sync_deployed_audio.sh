#!/bin/bash
set -euo pipefail

REMOTE_USER="${DEPLOYMENT_REMOTE_USER:-professionalpractice}"
REMOTE_HOST="${DEPLOYMENT_REMOTE_HOST:-merah.cassia.ifost.org.au}"
REMOTE_DIR="${DEPLOYMENT_REMOTE_DIR:-/var/www/vhosts/professional-practice.industrial-linguistics.com/htdocs}"
DEST_DIR="${SYNC_AUDIO_DEST_DIR:-content}"
MIN_AUDIO_TOPICS="${SYNC_MIN_AUDIO_TOPICS:-${DEPLOY_MIN_AUDIO_TOPICS:-5}}"
SSH_KEY="${DEPLOYMENT_SSH_KEY:-}"
if [ -z "$SSH_KEY" ] && [ -f "$HOME/.ssh/id_ed25519_merah" ]; then
  SSH_KEY="$HOME/.ssh/id_ed25519_merah"
fi

if [ -n "$SSH_KEY" ]; then
  RSYNC_SSH=(ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no)
else
  RSYNC_SSH=(ssh)
fi

mkdir -p "$DEST_DIR"
rsync -avz -e "${RSYNC_SSH[*]}" \
  --include='*/' \
  --include='audio.mp3' \
  --exclude='*' \
  "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/elearning/media/" \
  "$DEST_DIR/"

audio_count="$(find "$DEST_DIR" -path '*/audio.mp3' -type f | wc -l | tr -d ' ')"
if [ "$audio_count" -lt "$MIN_AUDIO_TOPICS" ]; then
  echo "only $audio_count deployed topic MP3 audio file(s) synced; expected at least $MIN_AUDIO_TOPICS" >&2
  exit 1
fi

echo "Synced $audio_count deployed topic MP3 audio file(s) into $DEST_DIR"
