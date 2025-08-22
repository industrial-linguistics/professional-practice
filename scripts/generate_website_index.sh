#!/bin/bash
set -e

SITE_DIR="website"
RUN_DIR="$SITE_DIR/run-script"
INDEX_FILE="$SITE_DIR/index.html"
CSS_FILE="$SITE_DIR/style.css"

mkdir -p "$SITE_DIR"

# Write CSS styling
cat > "$CSS_FILE" <<'EOT'
body { font-family: Arial, sans-serif; margin: 2rem; background-color: #f4f4f4; color: #333; }
h1 { color: #222; }
.part-list { list-style: none; padding: 0; }
.part-list li { background: #fff; margin: 1rem 0; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.part-list a { text-decoration: none; color: #007acc; font-size: 1.2rem; }
.part-list p { margin: 0.5rem 0 0; }
EOT

# Begin HTML file
cat > "$INDEX_FILE" <<EOT
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Professional Practice Run Scripts</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Professional Practice Run Scripts</h1>
  <ul class="part-list">
EOT

shopt -s nullglob
for outline in content/part-*/outline.md; do
  [ -f "$outline" ] || continue
  part_dir=$(dirname "$outline")
  part=$(basename "$part_dir")
  title=$(sed -n 's/^# Part [0-9]*[[:space:]][–-][[:space:]]*//p' "$outline")
  summary=$(awk 'NR>1 && NF {print; exit}' "$outline")
  printf '    <li><a href="run-script/%s/">%s</a><p>%s</p></li>\n' "$part" "$title" "$summary" >> "$INDEX_FILE"
done
shopt -u nullglob

cat >> "$INDEX_FILE" <<EOT
  </ul>
</body>
</html>
EOT

printf 'Generated %s and %s\n' "$INDEX_FILE" "$CSS_FILE"
