#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT=${REPO_ROOT:-"$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"}
cd "$REPO_ROOT"
if [[ $# -eq 0 ]]; then
  echo "Usage: scripts/image_review_publish_candidates.sh --candidate ID --format html --qa-passed [--run-id ID]" >&2
  echo "Fetch a current snapshot first with scripts/image_review_exchange.py fetch." >&2
  exit 2
fi
# A pending S3 submission is not yet a published candidate: check its receipt.
exec python3 scripts/image_review_exchange.py submit "$@"
