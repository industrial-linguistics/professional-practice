#!/usr/bin/env python3
"""Build KDP-ready paperback and eBook covers from canonical metadata."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "content" / "textbook-metadata.json"
INTERIOR = ROOT / "textbook" / "main-amazon.pdf"
OUTPUT = ROOT / "textbook" / "kdp"

TRIM_WIDTH = 6.0
TRIM_HEIGHT = 9.0
BLEED = 0.125
WHITE_PAPER_SPINE_PER_PAGE = 0.002252
DPI = 300

NAVY = "#071927"
INK = "#0D2538"
TEAL = "#39D1C1"
CORAL = "#FF7A59"
GOLD = "#F5C84C"
PAPER = "#F4F1E8"
MIST = "#C9D8DE"


def command_output(*args: str) -> str:
    return subprocess.check_output(args, text=True)


def page_count() -> int:
    match = re.search(r"^Pages:\s+(\d+)$", command_output("pdfinfo", str(INTERIOR)), re.M)
    if not match:
        raise RuntimeError(f"Could not read page count from {INTERIOR}")
    pages = int(match.group(1))
    return pages if pages % 2 == 0 else pages + 1


def text_lines(
    lines: list[str],
    *,
    x: float,
    y: float,
    size: float,
    leading: float,
    fill: str,
    weight: int = 400,
    anchor: str = "start",
    family: str = "Arial, Helvetica, sans-serif",
    letter_spacing: float = 0,
) -> str:
    spans = "".join(
        f'<tspan x="{x:.2f}" dy="{0 if i == 0 else leading:.2f}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" fill="{fill}" font-family="{family}" '
        f'font-size="{size:.2f}" font-weight="{weight}" text-anchor="{anchor}" '
        f'letter-spacing="{letter_spacing:.2f}">{spans}</text>'
    )


def topology_motif(x: float, y: float, scale: float = 1.0) -> str:
    nodes = [
        (0, 130, TEAL),
        (210, 0, GOLD),
        (440, 115, CORAL),
        (360, 360, TEAL),
        (105, 410, CORAL),
        (235, 220, PAPER),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5)]
    parts = [f'<g transform="translate({x:.2f} {y:.2f}) scale({scale:.4f})">']
    for a, b in edges:
        x1, y1, _ = nodes[a]
        x2, y2, _ = nodes[b]
        parts.append(
            f'<path d="M{x1} {y1} C{(x1+x2)/2:.1f} {y1}, {(x1+x2)/2:.1f} {y2}, {x2} {y2}" '
            f'fill="none" stroke="{MIST}" stroke-opacity="0.55" stroke-width="5"/>'
        )
    for nx, ny, colour in nodes:
        parts.append(f'<circle cx="{nx}" cy="{ny}" r="23" fill="{colour}"/>')
        parts.append(f'<circle cx="{nx}" cy="{ny}" r="38" fill="none" stroke="{colour}" stroke-opacity="0.30" stroke-width="4"/>')
    parts.append("</g>")
    return "".join(parts)


def front_panel(width: float, height: float, *, offset_x: float = 0) -> str:
    pad = width * 0.105
    title_y = height * 0.19
    return "".join(
        [
            f'<rect x="{offset_x}" y="0" width="{width}" height="{height}" fill="{NAVY}"/>',
            f'<rect x="{offset_x}" y="0" width="{width * 0.035}" height="{height}" fill="{TEAL}"/>',
            f'<circle cx="{offset_x + width * 0.92}" cy="{height * 0.08}" r="{width * 0.21}" fill="{INK}"/>',
            text_lines(
                ["IT", "PROFESSIONAL", "PRACTICE"],
                x=offset_x + pad,
                y=title_y,
                size=width * 0.093,
                leading=width * 0.105,
                fill=PAPER,
                weight=700,
                letter_spacing=width * 0.0025,
            ),
            f'<rect x="{offset_x + pad}" y="{height * 0.47}" width="{width * 0.16}" height="{height * 0.010}" fill="{CORAL}"/>',
            text_lines(
                [
                    "HOW DIGITAL SERVICES ARE",
                    "OPERATED, IMPROVED,",
                    "BOUGHT AND GOVERNED",
                ],
                x=offset_x + pad,
                y=height * 0.53,
                size=width * 0.034,
                leading=width * 0.048,
                fill=MIST,
                weight=600,
                letter_spacing=width * 0.0012,
            ),
            topology_motif(offset_x + width * 0.55, height * 0.66, width / 780),
            text_lines(
                ["GREG BAKER"],
                x=offset_x + pad,
                y=height * 0.91,
                size=width * 0.035,
                leading=0,
                fill=PAPER,
                weight=600,
                letter_spacing=width * 0.003,
            ),
        ]
    )


def ebook_svg() -> str:
    width, height = 1600.0, 2560.0
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f"{front_panel(width, height)}"
        "</svg>"
    )


def paperback_svg(pages: int) -> tuple[str, float, float]:
    spine_in = pages * WHITE_PAPER_SPINE_PER_PAGE
    total_width_in = BLEED + TRIM_WIDTH + spine_in + TRIM_WIDTH + BLEED
    total_height_in = BLEED + TRIM_HEIGHT + BLEED
    width = total_width_in * DPI
    height = total_height_in * DPI
    bleed = BLEED * DPI
    panel = TRIM_WIDTH * DPI
    spine = spine_in * DPI
    back_x = bleed
    spine_x = back_x + panel
    front_x = spine_x + spine

    blurb = [
        "Code is only one part of a dependable digital service.",
        "",
        "This practical guide connects the work that technical",
        "people are expected to understand but are rarely taught",
        "together: IT service management, delivery performance,",
        "incident learning, technology sales, vendor control,",
        "small-organisation IT, open source and data authority.",
        "",
        "Workplace cases and practice artefacts show how a ticket",
        "becomes a change, a sales promise becomes an operating",
        "obligation, an incident becomes evidence, and a service",
        "design survives questions about cost, risk and governance.",
        "",
        "For new and early-career practitioners who need to take",
        "part in the whole service conversation.",
    ]
    back_text = []
    y = height * 0.22
    for line in blurb:
        if not line:
            y += 42
            continue
        back_text.append(
            text_lines(
                [line],
                x=back_x + 155,
                y=y,
                size=35,
                leading=0,
                fill=INK,
                weight=400,
            )
        )
        y += 52

    barcode_w = 2.15 * DPI
    barcode_h = 1.35 * DPI
    barcode_x = spine_x - barcode_w - 90
    barcode_y = height - bleed - barcode_h - 80

    svg = "".join(
        [
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{total_width_in * 72:.4f}pt" height="{total_height_in * 72:.4f}pt" '
                f'viewBox="0 0 {width:.4f} {height:.4f}">'
            ),
            f'<rect width="{width:.4f}" height="{height:.4f}" fill="{PAPER}"/>',
            f'<rect x="{back_x:.2f}" y="0" width="{panel:.2f}" height="{height:.2f}" fill="{PAPER}"/>',
            f'<rect x="{back_x:.2f}" y="0" width="{panel:.2f}" height="{height * 0.08:.2f}" fill="{TEAL}"/>',
            text_lines(
                ["BEYOND THE CODE"],
                x=back_x + 155,
                y=height * 0.14,
                size=61,
                leading=0,
                fill=INK,
                weight=700,
                letter_spacing=2,
            ),
            *back_text,
            topology_motif(back_x + 160, height * 0.70, 0.58),
            f'<rect x="{barcode_x:.2f}" y="{barcode_y:.2f}" width="{barcode_w:.2f}" height="{barcode_h:.2f}" rx="9" fill="#FFFFFF"/>',
            f'<rect x="{spine_x:.2f}" y="0" width="{spine:.2f}" height="{height:.2f}" fill="{INK}"/>',
            (
                f'<text x="{spine_x + spine / 2:.2f}" y="{height / 2:.2f}" '
                f'fill="{PAPER}" font-family="Arial, Helvetica, sans-serif" font-size="38" '
                f'font-weight="700" text-anchor="middle" letter-spacing="1.2" '
                f'transform="rotate(90 {spine_x + spine / 2:.2f} {height / 2:.2f})">'
                "IT PROFESSIONAL PRACTICE  •  GREG BAKER</text>"
            ),
            front_panel(panel, height, offset_x=front_x),
            "</svg>",
        ]
    )
    return svg, total_width_in, total_height_in


def run() -> None:
    if not INTERIOR.exists():
        raise SystemExit(f"Build {INTERIOR.relative_to(ROOT)} before the cover.")
    if not shutil.which("rsvg-convert"):
        raise SystemExit("rsvg-convert is required.")
    if not shutil.which("convert"):
        raise SystemExit("ImageMagick convert is required.")

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    if metadata["title"] != "IT Professional Practice" or metadata["author"] != "Greg Baker":
        raise SystemExit("Cover copy must be reviewed before changing canonical title or author.")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    pages = page_count()

    ebook_source = OUTPUT / "ebook-cover.svg"
    ebook_png = OUTPUT / "ebook-cover.png"
    ebook_jpg = OUTPUT / "ebook-cover.jpg"
    ebook_source.write_text(ebook_svg(), encoding="utf-8")
    subprocess.run(
        [
            "rsvg-convert",
            "-f",
            "png",
            "-w",
            "1600",
            "-h",
            "2560",
            "-o",
            str(ebook_png),
            str(ebook_source),
        ],
        check=True,
    )
    subprocess.run(
        ["convert", str(ebook_png), "-quality", "96", "-colorspace", "sRGB", str(ebook_jpg)],
        check=True,
    )

    paperback, width_in, height_in = paperback_svg(pages)
    paperback_source = OUTPUT / "paperback-cover.svg"
    paperback_pdf = OUTPUT / "paperback-cover.pdf"
    paperback_source.write_text(paperback, encoding="utf-8")
    subprocess.run(
        ["rsvg-convert", "-f", "pdf", "-o", str(paperback_pdf), str(paperback_source)],
        check=True,
    )

    (OUTPUT / "cover-spec.txt").write_text(
        "\n".join(
            [
                f"Interior pages (rounded to even): {pages}",
                f"Trim: {TRIM_WIDTH:.3f} x {TRIM_HEIGHT:.3f} in",
                "Interior: black ink on white paper, no bleed",
                f"Spine: {pages} x {WHITE_PAPER_SPINE_PER_PAGE:.6f} = {pages * WHITE_PAPER_SPINE_PER_PAGE:.6f} in",
                f"Full cover with bleed: {width_in:.6f} x {height_in:.6f} in",
                "KDP should add the barcode in the reserved white area.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Built eBook cover (1600 x 2560 px) and {width_in:.6f} x {height_in:.6f} in paperback cover")


if __name__ == "__main__":
    run()
