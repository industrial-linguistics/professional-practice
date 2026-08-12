#!/bin/sh
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE="${IMAGE_REVIEW_REMOTE:-professionalpractice@merah.cassia.ifost.org.au}"
REMOTE_BUILD="${IMAGE_REVIEW_REMOTE_BUILD:-/home/professionalpractice/image-review-cgi-build}"
REMOTE_CGI="${IMAGE_REVIEW_REMOTE_CGI:-/var/www/vhosts/professional-practice.industrial-linguistics.com/cgi-bin/image-review.cgi}"
REMOTE_GO="${REMOTE_GO:-/usr/local/go1.26.5/bin/go}"
SSH_KEY="${IMAGE_REVIEW_SSH_KEY:-${DEPLOYMENT_SSH_KEY:-}}"

if [ -n "$SSH_KEY" ]; then
  ssh -i "$SSH_KEY" -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=20 "$REMOTE" "mkdir -p '$REMOTE_BUILD/cmd/image-review-cgi' '$REMOTE_BUILD/image-review'"
  rsync -a --delete -e "ssh -i $SSH_KEY -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=20" \
    "$ROOT/cmd/image-review-cgi/" \
    "$REMOTE:$REMOTE_BUILD/cmd/image-review-cgi/"
  rsync -a -e "ssh -i $SSH_KEY -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=20" \
    "$ROOT/go.mod" "$ROOT/go.sum" "$REMOTE:$REMOTE_BUILD/"
  rsync -a -e "ssh -i $SSH_KEY -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=20" \
    "$ROOT/image-review/review.css" "$REMOTE:$REMOTE_BUILD/image-review/"
  SSH_ARGS="-i $SSH_KEY -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=20"
else
  ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=20 "$REMOTE" "mkdir -p '$REMOTE_BUILD/cmd/image-review-cgi' '$REMOTE_BUILD/image-review'"
  rsync -a --delete -e "ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=20" \
    "$ROOT/cmd/image-review-cgi/" \
    "$REMOTE:$REMOTE_BUILD/cmd/image-review-cgi/"
  rsync -a -e "ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=20" \
    "$ROOT/go.mod" "$ROOT/go.sum" "$REMOTE:$REMOTE_BUILD/"
  rsync -a -e "ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=20" \
    "$ROOT/image-review/review.css" "$REMOTE:$REMOTE_BUILD/image-review/"
  SSH_ARGS="-o ServerAliveInterval=30 -o ServerAliveCountMax=20"
fi

# Intentional word splitting: SSH_ARGS is either empty or a fixed set of ssh options.
# shellcheck disable=SC2086
ssh $SSH_ARGS "$REMOTE" "
  set -eu
  test -x '$REMOTE_GO'
  export GOTOOLCHAIN=local
  cd '$REMOTE_BUILD'
  '$REMOTE_GO' test ./cmd/image-review-cgi
  '$REMOTE_GO' build -trimpath -o image-review.cgi ./cmd/image-review-cgi
  install -m 755 image-review.cgi '$REMOTE_CGI'
  '$REMOTE_GO' version -m '$REMOTE_CGI' | sed -n '1,4p'
"
