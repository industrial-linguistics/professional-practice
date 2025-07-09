#!/bin/bash
set -e
OUTPUT_DIR="website/run-script"
mkdir -p "$OUTPUT_DIR"
INDEX_FILE="$OUTPUT_DIR/index.html"
echo '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Run Script Resources</title></head><body><h1>Run Script Resources</h1><ul>' > "$INDEX_FILE"
for pdf in run-sheets/*.pdf; do
  [ -f "$pdf" ] || continue
  base=$(basename "$pdf" .pdf)
  dest_pdf="$OUTPUT_DIR/$base.pdf"
  cp "$pdf" "$dest_pdf"
  html_dir="$OUTPUT_DIR/$base"
  mkdir -p "$html_dir"
  pdftohtml -c -s -noframes "$pdf" "$html_dir/page" > /dev/null
  mv "$html_dir/page.html" "$html_dir/index.html"
  echo "<li><a href=\"$base.pdf\">$base.pdf</a> (<a href=\"$base/\">HTML</a>)</li>" >> "$INDEX_FILE"
  echo "Converted $pdf to HTML in $html_dir"
done
echo '</ul></body></html>' >> "$INDEX_FILE"
