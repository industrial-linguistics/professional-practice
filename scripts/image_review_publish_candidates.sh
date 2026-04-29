#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=${REPO_ROOT:-"$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"}
REMOTE=${IMAGE_REVIEW_REMOTE:-professionalpractice@merah}
SITE=${IMAGE_REVIEW_SITE:-professional-practice.industrial-linguistics.com}
VHOST=${IMAGE_REVIEW_VHOST:-/var/www/vhosts/$SITE}
STATE_DIR=${IMAGE_REVIEW_STATE_DIR:-state/image-review}
DB_PATH="$STATE_DIR/image-review.sqlite"
CANDIDATE_DIR="$STATE_DIR/candidates"

cd "$REPO_ROOT"

if [[ ! -f "$DB_PATH" ]]; then
  echo "No local image-review database found at $DB_PATH"
  exit 1
fi

ssh "$REMOTE" "mkdir -p '$VHOST/htdocs/image-review/candidates' '$VHOST/db' && chmod 775 '$VHOST/db'"
rsync -a "$CANDIDATE_DIR/" "$REMOTE:$VHOST/htdocs/image-review/candidates/"
scp "$DB_PATH" "$REMOTE:$VHOST/db/image-review.sqlite"
ssh "$REMOTE" "chmod 664 '$VHOST/db/image-review.sqlite'"
