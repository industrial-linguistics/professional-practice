#!/bin/bash
set -e
REMOTE_USER="professionalpractice"
REMOTE_HOST="merah.cassia.ifost.org.au"
REMOTE_DIR="/var/www/vhosts/professional-practice.industrial-linguistics.com/htdocs"
SSH_KEY="$DEPLOYMENT_SSH_KEY"

if [ -z "$SSH_KEY" ]; then
  echo "DEPLOYMENT_SSH_KEY is not set" >&2
  exit 1
fi

RSYNC_SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no"
rsync -avz -e "$RSYNC_SSH" website/ "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"
