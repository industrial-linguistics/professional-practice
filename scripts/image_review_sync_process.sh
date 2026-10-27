#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=${REPO_ROOT:-"$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"}
REMOTE=${IMAGE_REVIEW_REMOTE:-professionalpractice@merah}
SITE=${IMAGE_REVIEW_SITE:-professional-practice.industrial-linguistics.com}
VHOST=${IMAGE_REVIEW_VHOST:-/var/www/vhosts/$SITE}
STATE_DIR=${IMAGE_REVIEW_STATE_DIR:-state/image-review}
DB_PATH="$STATE_DIR/image-review.sqlite"
CANDIDATE_DIR="$STATE_DIR/candidates"
REMOTE_TMP="/tmp/${SITE}-image-review-$$.sqlite"
REMOTE_SCRIPT=${IMAGE_REVIEW_REMOTE_SCRIPT:-/home/professionalpractice/image-review-exchange/scripts/image_review_exchange.py}

cd "$REPO_ROOT"
mkdir -p "$STATE_DIR" "$CANDIDATE_DIR" logs

if ! ssh "$REMOTE" "test -f '$VHOST/db/image-review.sqlite'"; then
  echo "No image-review database exists on merah yet: $VHOST/db/image-review.sqlite"
  exit 0
fi

ssh "$REMOTE" "chmod 775 '$VHOST/db'"
ssh "$REMOTE" "sqlite3 '$VHOST/db/image-review.sqlite' \".backup '$REMOTE_TMP'\""
scp "$REMOTE:$REMOTE_TMP" "$DB_PATH"
ssh "$REMOTE" "rm -f '$REMOTE_TMP'"

rsync -a "$REMOTE:$VHOST/htdocs/image-review/candidates/" "$CANDIDATE_DIR/"

python3 scripts/image_review_process_reviews.py \
  --db "$DB_PATH" \
  --repo-root "$REPO_ROOT" \
  --candidates-dir "$CANDIDATE_DIR" \
  --rework-file image-review/rework-queue.md

# Merge acknowledgements for unchanged decisions. Never replace the live DB.
scp "$DB_PATH" "$REMOTE:$REMOTE_TMP"
ssh "$REMOTE" "python3 '$REMOTE_SCRIPT' authority-ack --db '$VHOST/db/image-review.sqlite' --processed-db '$REMOTE_TMP'"
ssh "$REMOTE" "rm -f '$REMOTE_TMP'"
