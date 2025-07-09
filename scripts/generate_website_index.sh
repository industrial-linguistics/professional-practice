#!/bin/bash
set -e
SITE_DIR="website"
INDEX_FILE="$SITE_DIR/index.html"

mkdir -p "$SITE_DIR"

# Begin HTML file
cat > "$INDEX_FILE" <<EOT
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Professional Practice Artifacts</title>
</head>
<body>
  <h1>Professional Practice Artifacts</h1>
  <ul>
EOT

shopt -s nullglob
entries=("$SITE_DIR"/*)
IFS=$'\n' sorted=($(sort <<<"${entries[*]}"))
unset IFS
for entry in "${sorted[@]}"; do
  name=$(basename "$entry")
  [ "$name" = "index.html" ] && continue
  if [ -d "$entry" ]; then
    echo "    <li><a href=\"$name/\">$name/</a></li>" >> "$INDEX_FILE"
  else
    echo "    <li><a href=\"$name\">$name</a></li>" >> "$INDEX_FILE"
  fi
done

cat >> "$INDEX_FILE" <<EOT
  </ul>
</body>
</html>
EOT

printf 'Generated %s\n' "$INDEX_FILE"
