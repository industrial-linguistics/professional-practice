#!/usr/bin/env python3
"""Build and validate a reflowable EPUB 3 from canonical textbook Markdown."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from build_textbook import book_part_title, book_topic_title
from course_content import ROOT, Part, Topic, load_course


CONTENT = ROOT / "content"
TEXTBOOK = ROOT / "textbook"
METADATA = CONTENT / "textbook-metadata.json"
REFERENCES = CONTENT / "textbook-references.bib"
CSS = CONTENT / "textbook-ebook.css"
COVER = TEXTBOOK / "kdp" / "ebook-cover.jpg"
OUTPUT = TEXTBOOK / "it-professional-practice.epub"
REPORT = TEXTBOOK / "audit" / "epubcheck.txt"
PREFACE = CONTENT / "textbook-preface.md"


COURSE_MAP = """\
The book moves through eight linked questions:

- **Promise:** What are we promising users, and what does good service look like?
- **Operating model:** Who receives work, escalates it, changes it, measures it and improves it?
- **Delivery pipeline:** How do we change the service repeatedly without making every release a crisis?
- **Incident learning:** What did the incident teach us about the system, and who owns the fix?
- **Vendor lifecycle:** What commercial promise has operations inherited, and what evidence keeps the relationship honest?
- **Small-organisation constraints:** Which controls matter first when money, time and specialist staff are scarce?
- **Data authority:** Who has authority to share, reuse, maintain and benefit from an artefact or dataset?
- **Service-design defence:** Can the design survive operational, commercial, technical and community questions?
"""


def read_metadata() -> dict[str, object]:
    return json.loads(METADATA.read_text(encoding="utf-8"))


def shift_topic_headings(markdown: str) -> str:
    return re.sub(
        r"^(#{2,4})(\s+)",
        lambda match: "#" + match.group(1) + match.group(2),
        markdown,
        flags=re.M,
    )


def ebook_image(source: Path, topic: Topic, asset_dir: Path) -> Path:
    """Return a Kindle-sized image without changing the print source."""
    if source.suffix.lower() != ".png" or source.stat().st_size <= 1_000_000:
        return source
    if not shutil.which("convert"):
        raise SystemExit("ImageMagick convert is required to optimise large EPUB images.")

    destination = asset_dir / f"{topic.part}-{topic.slug}-{source.stem}.jpg"
    subprocess.run(
        [
            "convert",
            str(source),
            "-resize",
            "1600x1600>",
            "-background",
            "white",
            "-alpha",
            "remove",
            "-alpha",
            "off",
            "-sampling-factor",
            "4:4:4",
            "-quality",
            "92",
            "-strip",
            str(destination),
        ],
        check=True,
    )
    return destination


def resolve_images(markdown: str, topic: Topic, asset_dir: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        alt, target = match.groups()
        if re.match(r"^[a-z]+:", target) or target.startswith("/"):
            return match.group(0)
        source = (topic.source_path / target).resolve()
        if not source.exists():
            raise FileNotFoundError(f"Missing EPUB image: {source}")
        return f"![{alt}]({ebook_image(source, topic, asset_dir)})"

    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", replace, markdown)


def topic_markdown(topic: Topic, asset_dir: Path) -> str:
    source = topic.source_path / "textbook.md"
    if not source.exists():
        raise FileNotFoundError(
            f"EPUB requires authored prose; missing {source.relative_to(ROOT)}"
        )
    body = source.read_text(encoding="utf-8")
    return resolve_images(shift_topic_headings(body), topic, asset_dir)


def part_markdown(part: Part, asset_dir: Path) -> str:
    blocks = [f"# {book_part_title(part)}"]
    intro = CONTENT / part.slug / "textbook-intro.md"
    if intro.exists():
        blocks.append(intro.read_text(encoding="utf-8"))
    for topic in part.topics:
        blocks.extend(
            [f"## {book_topic_title(topic)}", topic_markdown(topic, asset_dir)]
        )
    practice = CONTENT / part.slug / "practice-artifact.md"
    if practice.exists():
        blocks.extend(
            [
                "## Practice Artefact",
                shift_topic_headings(practice.read_text(encoding="utf-8")),
            ]
        )
    return "\n\n".join(blocks)


def copyright_page(metadata: dict[str, object]) -> str:
    isbn = str(metadata.get("ebook_isbn", "")).strip()
    isbn_line = f"\n\nKindle eBook ISBN: {isbn}" if isbn else ""
    return f"""\
# Copyright {{.unnumbered}}

::: copyright
Copyright © {metadata["year"]} {metadata["author"]}

All rights reserved.

{metadata["edition"]}, {metadata["year"]}

Published by {metadata["publisher"]}{isbn_line}

The examples and case organisations identified as fictional are teaching
devices. Product names and trademarks belong to their respective owners.
OCAP® is a registered trademark of the First Nations Information Governance
Centre.

This book provides professional-practice education, not legal, financial,
security or cultural-authority advice. Verify current rules and seek qualified
advice for decisions that carry material consequences.
:::
"""


def manuscript(
    metadata: dict[str, object],
    parts: list[Part],
    asset_dir: Path,
) -> str:
    preface = PREFACE.read_text(encoding="utf-8").replace(
        "{{course-map}}", COURSE_MAP
    )
    sections = [
        copyright_page(metadata),
        "# About This Book {.unnumbered}",
        preface,
    ]
    sections.extend(part_markdown(part, asset_dir) for part in parts)
    sections.extend(["# References {.unnumbered}", "::: {#refs}", ":::"])
    return "\n\n".join(sections) + "\n"


def pandoc_command(source: Path, metadata: dict[str, object]) -> list[str]:
    identifier = str(metadata.get("ebook_isbn", "")).strip()
    if identifier:
        identifier = f"urn:isbn:{identifier}"
    else:
        identifier = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, str(metadata['title']) + '|' + str(metadata['author']))}"
    return [
        "pandoc",
        str(source),
        "--from=markdown+smart+fenced_divs",
        "--to=epub3",
        "--standalone",
        "--toc",
        "--toc-depth=2",
        "--split-level=1",
        "--citeproc",
        f"--bibliography={REFERENCES}",
        f"--css={CSS}",
        f"--epub-cover-image={COVER}",
        f"--metadata=title:{metadata['title']}",
        f"--metadata=subtitle:{metadata['subtitle']}",
        f"--metadata=author:{metadata['author']}",
        f"--metadata=publisher:{metadata['publisher']}",
        f"--metadata=date:{metadata['year']}",
        f"--metadata=lang:{metadata['language']}",
        f"--metadata=identifier:{identifier}",
        f"--metadata=rights:Copyright © {metadata['year']} {metadata['author']}. All rights reserved.",
        "--metadata=link-citations:true",
        f"--output={OUTPUT}",
    ]


def validate() -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if not shutil.which("epubcheck"):
        REPORT.write_text("EPUBCheck not installed; validation not run.\n", encoding="utf-8")
        raise SystemExit("EPUBCheck is required for a release build.")
    result = subprocess.run(
        ["epubcheck", "--failonwarnings", str(OUTPUT)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    REPORT.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise SystemExit(result.stdout)


def build() -> None:
    if not shutil.which("pandoc"):
        raise SystemExit("Pandoc is required.")
    if not COVER.exists():
        raise SystemExit(
            f"Build {COVER.relative_to(ROOT)} with scripts/build_kdp_cover.py first."
        )
    metadata = read_metadata()
    parts = load_course()
    TEXTBOOK.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="professional-practice-epub-") as temp:
        temp_dir = Path(temp)
        asset_dir = temp_dir / "images"
        asset_dir.mkdir()
        source = temp_dir / "book.md"
        source.write_text(manuscript(metadata, parts, asset_dir), encoding="utf-8")
        subprocess.run(pandoc_command(source, metadata), check=True)
    validate()
    print(f"Built and validated {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
