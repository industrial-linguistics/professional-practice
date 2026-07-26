#!/usr/bin/env python3
"""Render deterministic image-review candidates and their slide previews."""

from __future__ import annotations

import argparse
import shutil
import struct
import subprocess
from pathlib import Path

from course_content import ROOT, read_text, section_fragments
from render_html_slides import chrome_path, render_page


def run_chrome(chrome: str, source: Path, output: Path, width: int, height: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        "--force-device-scale-factor=1",
        "--virtual-time-budget=1000",
        f"--window-size={width},{height}",
        f"--screenshot={output.resolve()}",
        source.resolve().as_uri(),
    ]
    subprocess.run(
        command,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"{path} is not a valid PNG")
    return struct.unpack(">II", data[16:24])


def render_bundle(candidate_dir: Path, chrome: str) -> None:
    candidate_dir = candidate_dir.resolve()
    candidate_source = candidate_dir / "candidate-source.html"
    slides_source = candidate_dir / "slides.html"
    prompt_source = candidate_dir / "prompt.txt"
    for required in (candidate_source, slides_source, prompt_source):
        if not required.is_file():
            raise SystemExit(f"Required review-bundle source is missing: {required}")

    slides = section_fragments(read_text(slides_source))
    if len(slides) != 2:
        raise SystemExit(f"{slides_source} must contain current and proposed slide sections")

    candidate_png = candidate_dir / "candidate.png"
    run_chrome(chrome, candidate_source, candidate_png, 1600, 900)

    scratch = ROOT / "output" / "image-review-render" / candidate_dir.name
    if scratch.exists():
        shutil.rmtree(scratch)
    (scratch / "images").mkdir(parents=True)
    shutil.copy2(candidate_png, scratch / "images" / "candidate.png")

    for fragment, name in zip(slides, ("current-slide", "proposed-slide"), strict=True):
        page = scratch / f"{name}.html"
        page.write_text(render_page(fragment), encoding="utf-8")
        run_chrome(chrome, page, candidate_dir / f"{name}.png", 1920, 1080)

    expected = {
        "candidate.png": (1600, 900),
        "current-slide.png": (1920, 1080),
        "proposed-slide.png": (1920, 1080),
    }
    for name, dimensions in expected.items():
        actual = png_dimensions(candidate_dir / name)
        if actual != dimensions:
            raise SystemExit(f"{candidate_dir / name} is {actual}, expected {dimensions}")
    print(f"Rendered image-review bundle: {candidate_dir.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_dirs", nargs="+", type=Path)
    args = parser.parse_args()
    chrome = chrome_path()
    for candidate_dir in args.candidate_dirs:
        render_bundle(candidate_dir, chrome)


if __name__ == "__main__":
    main()
