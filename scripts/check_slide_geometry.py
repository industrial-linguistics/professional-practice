#!/usr/bin/env python3
"""Check rendered HTML slides for containment, overlap and overflow defects."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from pathlib import Path

from course_content import ROOT, load_topic
from render_html_slides import chrome_path, render_page


QA_SCRIPT = r"""
<script>
(() => {
  const issues = [];
  const tolerance = 1.5;
  const targetWidth = 1920;
  const targetHeight = 1080;
  const boxSelector = [
    '.dg-card', '.dg-stage', '.dg-control', '.dg-proof', '.dg-panel',
    '.dg-gate-lead', '.dg-risk', '.dg-outcome', '.dg-question',
    '.dg-current', '.dg-target', '.dg-return-path'
  ].join(',');
  const boxes = Array.from(document.querySelectorAll(boxSelector));
  const label = (element) => {
    const text = (element.textContent || '').replace(/\s+/g, ' ').trim();
    return `${element.tagName.toLowerCase()}.${element.className || ''}:${text.slice(0, 70)}`;
  };
  const slide = document.querySelector('.slide');
  if (!slide) issues.push('missing .slide element');
  if (document.documentElement.scrollWidth > targetWidth + tolerance ||
      document.documentElement.scrollHeight > targetHeight + tolerance) {
    issues.push(`page overflow ${document.documentElement.scrollWidth}x${document.documentElement.scrollHeight} in ${targetWidth}x${targetHeight}`);
  }
  if (slide && (slide.scrollWidth > slide.clientWidth + tolerance || slide.scrollHeight > slide.clientHeight + tolerance)) {
    issues.push(`slide overflow ${slide.scrollWidth}x${slide.scrollHeight} in ${slide.clientWidth}x${slide.clientHeight}`);
  }
  for (const box of boxes) {
    if (box.scrollWidth > box.clientWidth + tolerance || box.scrollHeight > box.clientHeight + tolerance) {
      issues.push(`box overflow ${label(box)}`);
    }
    const rect = box.getBoundingClientRect();
    const style = getComputedStyle(box);
    const inset = {
      left: parseFloat(style.paddingLeft) || 0,
      right: parseFloat(style.paddingRight) || 0,
      top: parseFloat(style.paddingTop) || 0,
      bottom: parseFloat(style.paddingBottom) || 0,
    };
    const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!(node.nodeValue || '').trim()) continue;
      const owner = node.parentElement && node.parentElement.closest(boxSelector);
      if (owner !== box) continue;
      const range = document.createRange();
      range.selectNodeContents(node);
      const textRect = range.getBoundingClientRect();
      if (!textRect.width || !textRect.height) continue;
      if (textRect.left < rect.left + inset.left - tolerance ||
          textRect.right > rect.right - inset.right + tolerance ||
          textRect.top < rect.top + inset.top - tolerance ||
          textRect.bottom > rect.bottom - inset.bottom + tolerance) {
        issues.push(`text lacks box padding ${label(box)} -> ${(node.nodeValue || '').trim().slice(0, 60)}`);
      }
    }
  }
  for (let i = 0; i < boxes.length; i += 1) {
    for (let j = i + 1; j < boxes.length; j += 1) {
      const a = boxes[i];
      const b = boxes[j];
      if (a.parentElement !== b.parentElement || a.contains(b) || b.contains(a)) continue;
      const ar = a.getBoundingClientRect();
      const br = b.getBoundingClientRect();
      const overlapWidth = Math.min(ar.right, br.right) - Math.max(ar.left, br.left);
      const overlapHeight = Math.min(ar.bottom, br.bottom) - Math.max(ar.top, br.top);
      if (overlapWidth > tolerance && overlapHeight > tolerance) {
        issues.push(`sibling boxes overlap ${label(a)} <> ${label(b)}`);
      }
    }
  }
  const external = Array.from(document.querySelectorAll('.slide > h1, .slide > h2, .dg-caption'));
  for (const box of boxes) {
    const br = box.getBoundingClientRect();
    for (const text of external) {
      if (box.contains(text) || text.contains(box)) continue;
      const tr = text.getBoundingClientRect();
      const overlapWidth = Math.min(br.right, tr.right) - Math.max(br.left, tr.left);
      const overlapHeight = Math.min(br.bottom, tr.bottom) - Math.max(br.top, tr.top);
      if (overlapWidth > tolerance && overlapHeight > tolerance) {
        issues.push(`box overlaps external text ${label(box)} <> ${label(text)}`);
      }
    }
  }
  const result = {
    requestedViewport: [targetWidth, targetHeight],
    browserInnerViewport: [window.innerWidth, window.innerHeight],
    slide: slide ? [slide.clientWidth, slide.clientHeight] : null,
    boxesChecked: boxes.length,
    connectorsFound: document.querySelectorAll('.dg-arrow, svg line, svg path, svg marker').length,
    issues,
  };
  document.getElementById('geometry-results').textContent = JSON.stringify(result);
})();
</script>
"""


def instrument(page: str) -> str:
    marker = '<pre id="geometry-results" hidden></pre>'
    return page.replace("</body>", f"{marker}{QA_SCRIPT}</body>")


def check_topic(topic_dir: Path, chrome: str) -> tuple[int, list[str]]:
    topic_dir = topic_dir.resolve()
    topic = load_topic(topic_dir.parent.name, topic_dir)
    scratch = ROOT / "output" / "slide-geometry" / topic_dir.parent.name / topic_dir.name
    scratch.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for slide in topic.slides:
        page_path = scratch / f"slide-{slide.n:03d}.html"
        page_path.write_text(instrument(render_page(slide.html)), encoding="utf-8")
        command = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--virtual-time-budget=1000",
            "--window-size=1920,1080",
            "--dump-dom",
            page_path.resolve().as_uri(),
        ]
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
        match = re.search(r'<pre id="geometry-results" hidden="">(.*?)</pre>', completed.stdout, re.DOTALL)
        if not match:
            match = re.search(r'<pre id="geometry-results" hidden>(.*?)</pre>', completed.stdout, re.DOTALL)
        if not match:
            failures.append(f"slide {slide.n}: browser returned no geometry result")
            continue
        result = json.loads(html.unescape(match.group(1)))
        if result["issues"]:
            failures.extend(f"slide {slide.n}: {issue}" for issue in result["issues"])
    return len(topic.slides), failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topics", nargs="+", type=Path)
    args = parser.parse_args()
    chrome = chrome_path()
    total = 0
    failures: list[str] = []
    for topic_dir in args.topics:
        count, topic_failures = check_topic(topic_dir, chrome)
        total += count
        failures.extend(f"{topic_dir}: {failure}" for failure in topic_failures)
    if failures:
        raise SystemExit("Geometry QA failed:\n" + "\n".join(failures))
    print(f"Geometry QA passed for {total} slide(s): no containment, overlap or overflow defects")


if __name__ == "__main__":
    main()
