#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SECRET_FILE=${IMAGE_REVIEW_BRIDGE_ENV:-$HOME/.config/professional-practice/image-review-bridge.env}
test -r "$SECRET_FILE"
set -a
source "$SECRET_FILE"
set +a
mkdir -p "$ROOT/state/image-review-bridge" "$ROOT/logs"
exec 9>"$ROOT/state/image-review-bridge/bridge.lock"
if ! flock -n 9; then exit 0; fi
CODE_ROOT=$ROOT
if [[ -d "$ROOT/repository/.git" ]]; then
  CODE_ROOT=$ROOT/repository
  git -C "$CODE_ROOT" fetch --quiet origin main
  git -C "$CODE_ROOT" merge --quiet --ff-only origin/main
fi
REMOTE=${IMAGE_REVIEW_REMOTE:-professionalpractice@merah}
REMOTE_SCRIPT=/home/professionalpractice/image-review-exchange/scripts/image_review_exchange.py
# Publish trusted main-branch helper code atomically, and keep review CSS current.
scp -q "$CODE_ROOT/scripts/image_review_exchange.py" "$REMOTE:$REMOTE_SCRIPT.new"
ssh -o BatchMode=yes "$REMOTE" "mv '$REMOTE_SCRIPT.new' '$REMOTE_SCRIPT'"
scp -q "$CODE_ROOT/image-review/review.css" "$REMOTE:/var/www/vhosts/professional-practice.industrial-linguistics.com/htdocs/image-review/review.css"
cd "$ROOT"
if summary=$("$ROOT/.venv/bin/python" "$CODE_ROOT/scripts/image_review_exchange.py" bridge); then
  printf '%s\n' "$summary" >> "$ROOT/logs/image-review-bridge.log"
else
  result=$?
  printf 'Image review exchange failed (exit %s)\n' "$result" >&2
  exit "$result"
fi
# Retain every run in the log; send cron mail for changes, imports or rejections.
printf '%s\n' "$summary" | "$ROOT/.venv/bin/python" -c '
import json,pathlib,sys
path=pathlib.Path(sys.argv[1]); current=json.load(sys.stdin)
previous=json.loads(path.read_text()) if path.exists() else {}
if current.get("accepted") or current.get("rejected") or previous.get("snapshot",{}).get("version") != current["snapshot"]["version"]:
    print(json.dumps(current,sort_keys=True))
temporary=path.with_suffix(".new");temporary.write_text(json.dumps(current));temporary.replace(path)
' "$ROOT/state/image-review-bridge/last-success.json"
