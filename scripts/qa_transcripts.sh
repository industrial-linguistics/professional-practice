#!/usr/bin/env bash
set -euo pipefail

OUTPUT_ROOT=${OUTPUT_ROOT:-build}
MODEL=${MODEL:-tiny}
THRESHOLD=${THRESHOLD:-0.82}

if ! command -v whisper >/dev/null 2>&1; then
  echo "whisper CLI not found; skipping transcription QA" >&2
  exit 0
fi

root_dir=$(cd "$(dirname "$0")/.." && pwd)
failures=0

while IFS= read -r narration; do
  lesson_dir=$(dirname "$narration")
  manifest="$lesson_dir/../manifests/timings.tsv"
  if [[ ! -f "$manifest" ]]; then
    echo "Skipping $narration (missing manifest)" >&2
    continue
  fi
  echo "Transcribing $(basename "$narration")"
  whisper "$narration" --model "$MODEL" --language en --output_dir "$lesson_dir" --output_format txt --fp16 False >/dev/null
  transcript_file="$lesson_dir/$(basename "$narration" .wav).txt"
  if [[ ! -f "$transcript_file" ]]; then
    echo "Failed to produce transcript for $narration" >&2
    failures=$((failures+1))
    continue
  fi
  expected=$(cut -f4 "$manifest" | tr '\n' ' ' | tr -s '[:space:]' ' ')
  actual=$(cat "$transcript_file" | tr '\n' ' ' | tr -s '[:space:]' ' ')
  score=$(EXPECTED="$expected" ACTUAL="$actual" python - <<'PY'
import os
from difflib import SequenceMatcher
expected=os.environ["EXPECTED"]
actual=os.environ["ACTUAL"]
ratio=SequenceMatcher(None, expected.lower(), actual.lower()).ratio()
print(f"{ratio:.4f}")
PY
)
  printf "Similarity: %s\n" "$score"
  awk "BEGIN {exit ($score < $THRESHOLD)}" || {
    echo "Mismatch detected for $narration" >&2
    failures=$((failures+1))
  }
done < <(find "$root_dir/$OUTPUT_ROOT" -name narration.wav | sort)

if [[ $failures -gt 0 ]]; then
  echo "$failures transcription checks failed" >&2
  exit 1
fi

echo "Transcription QA passed"
