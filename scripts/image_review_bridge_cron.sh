#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SECRET_FILE=${IMAGE_REVIEW_BRIDGE_ENV:-$HOME/.config/professional-practice/image-review-bridge.env}
test -r "$SECRET_FILE"
set -a
source "$SECRET_FILE"
set +a
mkdir -p "$ROOT/state/image-review-bridge"
exec 9>"$ROOT/state/image-review-bridge/bridge.lock"
if ! flock -n 9; then
  echo "Image review bridge already running; skipped overlap"
  exit 0
fi
cd "$ROOT"
exec "$ROOT/.venv/bin/python" scripts/image_review_exchange.py bridge
