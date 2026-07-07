#!/bin/bash
set -e

SITE_DIR="website"
RUN_DIR="$SITE_DIR/run-script"
INDEX_FILE="$SITE_DIR/index.html"
CSS_FILE="$SITE_DIR/style.css"

mkdir -p "$SITE_DIR"

# Write CSS styling
cat > "$CSS_FILE" <<'EOT'
body { font-family: Arial, sans-serif; margin: 0; background-color: #f4f4f4; color: #333; }
.hero { padding: 3rem 2rem; color: #fff; background: #243447; }
.hero nav { display: flex; gap: .75rem; flex-wrap: wrap; margin-bottom: 2rem; }
.hero nav a { color: #fff; border: 1px solid rgba(255,255,255,.35); border-radius: 999px; padding: .5rem .75rem; text-decoration: none; }
.hero p { max-width: 56rem; font-size: 1.15rem; line-height: 1.5; }
h1 { max-width: 58rem; margin: 0 0 1rem; color: #fff; font-size: clamp(2.2rem, 6vw, 4.6rem); line-height: .98; }
.positioning { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 1rem; max-width: 70rem; margin-top: 2rem; }
.positioning div { border: 1px solid rgba(255,255,255,.25); border-radius: 8px; padding: 1rem; background: rgba(255,255,255,.08); }
.positioning strong { display: block; margin-bottom: .5rem; text-transform: uppercase; letter-spacing: .08em; font-size: .78rem; }
.main { margin: 2rem; }
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
  <title>IT Professional Practice</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="hero">
    <nav>
      <a href="run-script/part-01/">Run scripts</a>
    </nav>
    <h1>The missing professional-practice course for technical graduates</h1>
    <p>IT Professional Practice is for students and early-career IT, data and software people learning how real digital services are operated, improved, bought, sold and stewarded. The run scripts below mirror the eight-part course while the generated e-learning and textbook surfaces mature.</p>
    <div class="positioning">
      <div><strong>For</strong> Graduates, support analysts, junior developers, data workers and technical staff moving into customer or vendor-facing roles.</div>
      <div><strong>About</strong> ITIL service practice, delivery pipelines, incident learning, CRM handoffs, vendor risk, startup constraints and data authority.</div>
      <div><strong>Output</strong> A professional-practice course reader, browser lessons, practical artefacts and a capstone service design.</div>
    </div>
  </header>
  <main class="main">
  <h2>Course Parts</h2>
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
  </main>
</body>
</html>
EOT

printf 'Generated %s and %s\n' "$INDEX_FILE" "$CSS_FILE"
