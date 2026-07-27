#!/usr/bin/env python3
"""Validate the generated paperback, cover and EPUB release files."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXTBOOK = ROOT / "textbook"
INTERIOR = TEXTBOOK / "main-amazon.pdf"
PAPERBACK_COVER = TEXTBOOK / "kdp" / "paperback-cover.pdf"
EBOOK_COVER = TEXTBOOK / "kdp" / "ebook-cover.jpg"
EPUB = TEXTBOOK / "it-professional-practice.epub"
EPUBCHECK = TEXTBOOK / "audit" / "epubcheck.txt"
KINDLE_SUMMARY = TEXTBOOK / "audit" / "kindle-previewer" / "Summary_Log.csv"
REPORT = TEXTBOOK / "audit" / "release-checks.txt"
METADATA = ROOT / "content" / "textbook-metadata.json"

TRIM_WIDTH_POINTS = 6 * 72
TRIM_HEIGHT_POINTS = 9 * 72
BLEED_HEIGHT_POINTS = 9.25 * 72
SPINE_PER_PAGE = 0.002252


class Checks:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.failures = 0

    def pass_(self, message: str) -> None:
        self.lines.append(f"PASS  {message}")

    def fail(self, message: str) -> None:
        self.lines.append(f"FAIL  {message}")
        self.failures += 1

    def expect(self, condition: bool, message: str) -> None:
        self.pass_(message) if condition else self.fail(message)


def output(*command: str) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True)


def pdf_field(text: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}:\s+(.+)$", text, re.M)
    if not match:
        raise ValueError(f"Missing pdfinfo field: {label}")
    return match.group(1).strip()


def page_size(text: str) -> tuple[float, float]:
    value = pdf_field(text, "Page size")
    match = re.match(r"([0-9.]+) x ([0-9.]+) pts", value)
    if not match:
        raise ValueError(f"Unexpected PDF page size: {value}")
    return float(match.group(1)), float(match.group(2))


def check_pdf(checks: Checks) -> int:
    info = output("pdfinfo", str(INTERIOR))
    pages = int(pdf_field(info, "Pages"))
    width, height = page_size(info)
    checks.expect(pages % 2 == 0, f"paperback has an even page count ({pages})")
    checks.expect(
        abs(width - TRIM_WIDTH_POINTS) < 0.2
        and abs(height - TRIM_HEIGHT_POINTS) < 0.2,
        f"paperback trim is 6 x 9 inches ({width:.2f} x {height:.2f} pt)",
    )
    checks.expect(pdf_field(info, "Encrypted") == "no", "paperback PDF is not encrypted")

    text = output("pdftotext", str(INTERIOR), "-")
    for required in (
        "IT Professional Practice",
        "Greg Baker",
        "Industrial Linguistics",
        "References",
        "Index",
        "Design and Defend an IT Service",
    ):
        checks.expect(required in text, f"paperback contains {required!r}")
    front_matter = output(
        "pdftotext",
        "-f",
        "1",
        "-l",
        "4",
        str(INTERIOR),
        "-",
    )
    draft_markers = ("draft copy", "not for distribution", "proof copy")
    checks.expect(
        not any(marker in front_matter.lower() for marker in draft_markers),
        "paperback front matter contains no draft or proof watermark",
    )

    font_rows = [
        line
        for line in output("pdffonts", str(INTERIOR)).splitlines()[2:]
        if line.strip()
    ]
    embedded = all(
        re.search(r"\s+yes\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$", line)
        for line in font_rows
    )
    checks.expect(bool(font_rows) and embedded, "all paperback fonts are embedded")

    image_rows = output("pdfimages", "-list", str(INTERIOR)).splitlines()[2:]
    ppis: list[tuple[int, int]] = []
    for line in image_rows:
        columns = line.split()
        if len(columns) >= 14 and columns[2] == "image":
            ppis.append((int(columns[12]), int(columns[13])))
    checks.expect(bool(ppis), f"paperback contains {len(ppis)} interior image(s)")
    checks.expect(
        bool(ppis) and all(300 <= x <= 600 and 300 <= y <= 600 for x, y in ppis),
        "all paperback raster images are between 300 and 600 effective PPI",
    )
    return pages


def check_cover(checks: Checks, pages: int) -> None:
    info = output("pdfinfo", str(PAPERBACK_COVER))
    width, height = page_size(info)
    expected_width = (
        0.125 + 6 + pages * SPINE_PER_PAGE + 6 + 0.125
    ) * 72
    checks.expect(int(pdf_field(info, "Pages")) == 1, "paperback cover is one page")
    checks.expect(
        abs(width - expected_width) < 0.2
        and abs(height - BLEED_HEIGHT_POINTS) < 0.2,
        "paperback cover dimensions match the final page count and 0.125-inch bleed",
    )

    cover_info = output(
        "identify",
        "-format",
        "%w %h %[colorspace]",
        str(EBOOK_COVER),
    ).strip()
    checks.expect(
        cover_info.lower() == "1600 2560 srgb",
        f"Kindle cover is 1600 x 2560 RGB ({cover_info})",
    )


def check_epub(checks: Checks, metadata: dict[str, object]) -> None:
    size = EPUB.stat().st_size
    checks.expect(size < 3_000_000, f"EPUB is below 3 MB ({size / 1_000_000:.2f} MB)")
    report = EPUBCHECK.read_text(encoding="utf-8")
    checks.expect(
        "0 fatals / 0 errors / 0 warnings" in report.lower(),
        "EPUBCheck reports zero fatal errors, errors and warnings",
    )
    with zipfile.ZipFile(EPUB) as archive:
        names = archive.namelist()
        first = archive.read(names[0])
        checks.expect(
            names[0] == "mimetype" and first == b"application/epub+zip",
            "EPUB has the required uncompressed mimetype entry first",
        )
        package = "\n".join(
            archive.read(name).decode("utf-8", errors="replace")
            for name in names
            if name.endswith((".opf", "nav.xhtml"))
        )
        for required in (
            str(metadata["title"]),
            str(metadata["author"]),
            str(metadata["publisher"]),
            "Design and Defend an IT Service",
            "References",
        ):
            checks.expect(required in package, f"EPUB metadata/navigation contains {required!r}")
        image_count = sum(
            name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))
            for name in names
        )
        checks.expect(image_count >= 5, f"EPUB contains its cover and interior images ({image_count})")


def check_kindle_previewer(checks: Checks) -> None:
    with KINDLE_SUMMARY.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    checks.expect(len(rows) == 1, "Kindle Previewer produced one conversion result")
    if len(rows) != 1:
        return
    row = rows[0]
    checks.expect(
        row.get("Conversion Status") == "Success",
        "Kindle Previewer conversion succeeded",
    )
    checks.expect(
        row.get("Enhanced Typesetting Status") == "Supported",
        "Kindle Enhanced Typesetting is supported",
    )
    checks.expect(row.get("Error Count") == "0", "Kindle Previewer reports zero errors")
    checks.expect(
        row.get("Quality Issue Count") == "0",
        "Kindle Previewer reports zero navigation-quality issues",
    )
    output_file = Path(row.get("Output File Path", ""))
    checks.expect(
        output_file.exists() and output_file.suffix.lower() == ".kpf",
        "Kindle Previewer produced a KPF device-preview package",
    )


def check_metadata(checks: Checks, metadata: dict[str, object]) -> None:
    required = ("title", "subtitle", "author", "publisher", "edition", "year", "language")
    checks.expect(
        all(str(metadata.get(field, "")).strip() for field in required),
        "canonical publication metadata is complete",
    )
    isbn = str(metadata.get("paperback_isbn", "")).replace("-", "").strip()
    checks.expect(
        not isbn or bool(re.fullmatch(r"(?:978|979)\d{10}", isbn)),
        "paperback ISBN is blank or a syntactically valid ISBN-13",
    )


def main() -> None:
    checks = Checks()
    required_files = (
        INTERIOR,
        PAPERBACK_COVER,
        EBOOK_COVER,
        EPUB,
        EPUBCHECK,
        KINDLE_SUMMARY,
        METADATA,
    )
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    if missing:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(
            "\n".join(f"FAIL  missing {path}" for path in missing) + "\n",
            encoding="utf-8",
        )
        raise SystemExit("Missing release files: " + ", ".join(missing))

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    check_metadata(checks, metadata)
    pages = check_pdf(checks)
    check_cover(checks, pages)
    check_epub(checks, metadata)
    check_kindle_previewer(checks)
    checks.lines.extend(
        [
            "",
            "EXTERNAL RELEASE GATES",
            "PENDING  Complete and record the Part 7 Indigenous content review.",
            "PENDING  Assign the paperback ISBN and rebuild, or choose KDP's free ISBN and accept the Independently published imprint.",
            "PENDING  Visually inspect the generated KPF in Kindle Previewer's phone, tablet and e-reader views.",
            "PENDING  Pass KDP Print Previewer and order/approve a physical proof.",
            "PENDING  Complete the KDP AI-generated-content disclosure.",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(checks.lines) + "\n", encoding="utf-8")
    print("\n".join(checks.lines))
    if checks.failures:
        raise SystemExit(f"{checks.failures} release check(s) failed.")


if __name__ == "__main__":
    main()
