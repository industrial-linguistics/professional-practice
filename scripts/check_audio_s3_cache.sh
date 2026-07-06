#!/usr/bin/env bash
set -euo pipefail

if [[ -f "$HOME/.profile" ]]; then
  # shellcheck disable=SC1090
  . "$HOME/.profile"
fi

if [[ -f "$HOME/.config/professional-practice.env" ]]; then
  # shellcheck disable=SC1090
  . "$HOME/.config/professional-practice.env"
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "aws CLI is not installed or not on PATH" >&2
  exit 1
fi

bucket=${VOICER_S3_BUCKET:-}
if [[ -z "$bucket" ]]; then
  echo "VOICER_S3_BUCKET is not set" >&2
  exit 1
fi

tmp=$(mktemp)
readback=$(mktemp)
cleanup() {
  rm -f "$tmp" "$readback"
}
trap cleanup EXIT

printf 'professional-practice-audio-cache-smoke\n' > "$tmp"
key="cache-smoke/$(hostname)-$(date -u +%Y%m%dT%H%M%SZ)-$$.txt"
identity=$(aws sts get-caller-identity --query Arn --output text)

aws s3api put-object --bucket "$bucket" --key "$key" --body "$tmp" >/dev/null
aws s3api get-object --bucket "$bucket" --key "$key" "$readback" >/dev/null
cmp "$tmp" "$readback" >/dev/null
aws s3api delete-object --bucket "$bucket" --key "$key" >/dev/null

echo "Audio S3 cache smoke test passed"
echo "  principal: $identity"
echo "  bucket: s3://$bucket"
echo "  key: $key"
