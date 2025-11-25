#!/usr/bin/env bash
set -euo pipefail

OUTPUT_ROOT=${OUTPUT_ROOT:-build}
root_dir=$(cd "$(dirname "$0")/.." && pwd)
out_dir="$root_dir/$OUTPUT_ROOT/ebooks"
mkdir -p "$out_dir"

combined="$out_dir/course.md"
: >"$combined"

parts=($(find "$root_dir/content" -maxdepth 1 -mindepth 1 -type d | sort))
for part_dir in "${parts[@]}"; do
  part=$(basename "$part_dir")
  printf "# %s\n\n" "${part//-/ }" >>"$combined"
  topics=($(find "$part_dir" -maxdepth 1 -mindepth 1 -type d | sort))
  for topic_dir in "${topics[@]}"; do
    topic=$(basename "$topic_dir")
    printf "## %s\n\n" "${topic//-/ }" >>"$combined"
    if [[ -f "$topic_dir/slides.md" ]]; then
      cat "$topic_dir/slides.md" >>"$combined"
      echo -e "\n" >>"$combined"
    fi
    if [[ -d "$topic_dir/narratives" ]]; then
      for f in $(find "$topic_dir/narratives" -type f -name '*.md' | sort); do
        echo "### $(basename "$f" .md)" >>"$combined"
        cat "$f" >>"$combined"
        echo -e "\n" >>"$combined"
      done
    fi
  done
done

echo "Combined course markdown written to $combined"

if command -v pandoc >/dev/null 2>&1; then
  pandoc "$combined" -o "$out_dir/course.pdf"
  pandoc "$combined" -o "$out_dir/course.epub"
  echo "Pandoc outputs written to $out_dir"
else
  echo "pandoc not found; skipped PDF/EPUB generation" >&2
fi
