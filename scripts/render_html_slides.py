#!/usr/bin/env python3
"""Render ``slides.html`` sections to PNG images for video/run-sheet tooling."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from build_elearning import COURSE_CSS
from course_content import CONTENT, ROOT, load_topic


SLIDE_IMAGES = ROOT / "assets" / "slide-images"


def chrome_path() -> str:
    for env_name in ["CHROME_PATH", "BROWSER_PATH", "MARP_BROWSER_PATH"]:
        configured = os.environ.get(env_name)
        if configured and Path(configured).exists():
            return configured
    candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        Path("/usr/bin/google-chrome"),
        Path("/usr/bin/chromium"),
        Path("/usr/bin/chromium-browser"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    for name in ["google-chrome", "chromium", "chromium-browser"]:
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Chrome/Chromium not found. Run scripts/install_chrome.sh or set up Chrome.")


def render_page(slide_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{COURSE_CSS}
html, body {{
  width: 1920px;
  height: 1080px;
  margin: 0;
  overflow: hidden;
  background: #101828;
}}
body {{
  display: grid;
  place-items: center;
}}
.slide {{
  width: 1760px;
  height: 990px;
  min-height: 990px;
  max-height: 990px;
  overflow: hidden;
  box-shadow: none;
}}
.slide h1,
.slide h2 {{
  font-size: 72px;
}}
.slide p,
.slide li,
.slide td,
.slide th {{
  font-size: 34px;
}}
.slide table {{
  table-layout: fixed;
}}
.slide pre {{
  font-size: 30px;
}}
.slide-figure img,
.slide img {{
  max-height: 690px;
}}
.slide .diagram {{
  font-size: 28px;
}}
</style>
</head>
<body>
{slide_html}
</body>
</html>
"""


def render_topic(topic_dir: Path, chrome: str) -> int:
    if not (topic_dir / "slides.html").exists():
        raise SystemExit(f"slides.html not found in {topic_dir}")
    part = topic_dir.parent.name
    topic = load_topic(part, topic_dir)
    out_dir = SLIDE_IMAGES / part / topic_dir.name
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    scratch = ROOT / "output" / "render-html-slides" / part / topic_dir.name
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    src_images = topic_dir / "images"
    if src_images.exists():
        shutil.copytree(src_images, scratch / "images")

    for slide in topic.slides:
        page = scratch / f"slide-{slide.n:03d}.html"
        page.write_text(render_page(slide.html), encoding="utf-8")
        out = out_dir / f"slide.{slide.n:03d}.png"
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--window-size=1920,1080",
            f"--screenshot={out}",
            page.resolve().as_uri(),
        ]
        if os.environ.get("PUPPETEER_DANGEROUS_NO_SANDBOX", "").lower() in {"1", "true", "yes"}:
            cmd.insert(1, "--no-sandbox")
            cmd.insert(2, "--disable-setuid-sandbox")
        if sys.platform.startswith("linux"):
            cmd.insert(3, "--disable-dev-shm-usage")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as error:
            detail = (error.stderr or "").strip()
            if detail:
                raise RuntimeError(f"Chrome failed while rendering {page}: {detail}") from error
            raise
    print(f"Rendered {len(topic.slides)} slide image(s) to {out_dir.relative_to(ROOT)}")
    return len(topic.slides)


def topic_dirs(content_dir: Path) -> list[Path]:
    return sorted(path.parent for path in content_dir.glob("part-*/*/slides.html"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("topics", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--content-dir", type=Path, default=CONTENT)
    args = parser.parse_args()
    if args.all:
        topics = topic_dirs(args.content_dir)
    else:
        topics = [path if path.is_dir() else path.parent for path in args.topics]
    if not topics:
        raise SystemExit("Specify topic directories or --all")
    chrome = chrome_path()
    total = 0
    for topic in topics:
        total += render_topic(topic, chrome)
    print(f"Rendered {total} slide image(s)")


if __name__ == "__main__":
    main()
