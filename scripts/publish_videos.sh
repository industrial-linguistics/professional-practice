#!/usr/bin/env bash
set -euo pipefail

REMOTE=${VIDEO_PUBLISH_REMOTE:-professionalpractice@merah}
SITE=${VIDEO_PUBLISH_SITE:-professional-practice.industrial-linguistics.com}
VHOST=${VIDEO_PUBLISH_VHOST:-/var/www/vhosts/$SITE}
REMOTE_DIR=${VIDEO_PUBLISH_REMOTE_DIR:-$VHOST/htdocs/videos}
STAGING_DIR=${VIDEO_PUBLISH_STAGING_DIR:-}

if [[ -z "$STAGING_DIR" ]]; then
  STAGING_DIR="$(mktemp -d)"
  CLEAN_STAGING=true
else
  CLEAN_STAGING=false
  mkdir -p "$STAGING_DIR"
fi

cleanup() {
  if [[ "${CLEAN_STAGING:-false}" == "true" ]]; then
    rm -rf "$STAGING_DIR"
  fi
}
trap cleanup EXIT

python3 - "$STAGING_DIR" <<'PY'
from __future__ import annotations

import html
import hashlib
import re
import shutil
import sys
import unicodedata
from pathlib import Path

staging = Path(sys.argv[1])
content = Path("content")
videos = sorted(content.glob("part-*/*/final.mp4"))

if not videos:
    raise SystemExit("No generated final.mp4 files found under content/part-*/*/")

if staging.exists():
    for child in staging.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
staging.mkdir(parents=True, exist_ok=True)


def title_for(topic_dir: Path) -> str:
    slides = topic_dir / "slides.md"
    if not slides.exists():
        return topic_dir.name.replace("-", " ").title()
    for line in slides.read_text(errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("title:"):
            return stripped.split(":", 1)[1].strip().strip('"')
    for line in slides.read_text(errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return topic_dir.name.replace("-", " ").title()


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "video"


rows = []
for src in videos:
    rel = src.parent.relative_to(content)
    part = rel.parts[0]
    topic = rel.parts[1]
    title = title_for(src.parent)
    filename = f"{part}-{slugify(title)}.mp4"
    dest = staging / rel / filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    size = src.stat().st_size
    version = hashlib.sha256(src.read_bytes()).hexdigest()[:12]
    rows.append(
        {
            "part": part,
            "topic": topic,
            "title": title,
            "href": f"{part}/{topic}/{filename}?v={version}",
            "size": size,
        }
    )


def fmt_size(size: int) -> str:
    return f"{size / 1024 / 1024:.1f} MiB"


index = staging / "index.html"
items = "\n".join(
    "      <li>"
    f"<a href=\"{html.escape(row['href'])}\">{html.escape(row['part'])} / "
    f"{html.escape(row['title'])}</a>"
    f"<span>{html.escape(fmt_size(row['size']))}</span>"
    "</li>"
    for row in rows
)
total_size = sum(row["size"] for row in rows)
index.write_text(
    f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Professional Practice Videos</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; background: #f4f4f4; color: #333; }}
    h1 {{ color: #222; }}
    .summary {{ color: #555; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ background: #fff; margin: 0.75rem 0; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; gap: 1rem; justify-content: space-between; align-items: baseline; }}
    a {{ color: #007acc; font-size: 1.1rem; text-decoration: none; }}
    span {{ color: #555; white-space: nowrap; }}
  </style>
</head>
<body>
  <h1>Professional Practice Videos</h1>
  <p class="summary">{len(rows)} generated lesson videos, {fmt_size(total_size)} total.</p>
  <ul>
{items}
  </ul>
</body>
</html>
""",
    encoding="utf-8",
)

print(f"Prepared {len(rows)} video(s), {fmt_size(total_size)} total, in {staging}")
PY

find "$STAGING_DIR" -type d -exec chmod 755 {} +
find "$STAGING_DIR" -type f -exec chmod 644 {} +

ssh "$REMOTE" "mkdir -p '$REMOTE_DIR'"
rsync -az --delete "$STAGING_DIR"/ "$REMOTE:$REMOTE_DIR"/
ssh "$REMOTE" "find '$REMOTE_DIR' -type d -exec chmod 755 {} + && find '$REMOTE_DIR' -type f -exec chmod 644 {} +"

echo "Published videos to $REMOTE:$REMOTE_DIR"
