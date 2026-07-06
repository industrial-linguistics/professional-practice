#!/usr/bin/env python3
"""Repair slide/narrative count mismatches with one narrative per slide.

The repair is deliberately conservative:
- matched topics are left untouched;
- existing root-level narrative files are copied into an archive subdirectory
  before the canonical files are written;
- uncovered slides receive concise generated narration based only on their
  slide text and topic title.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from course_content import ROOT, Slide, Topic, load_course, markdown_to_plain, narrative_files
from report_narrative_mismatches import align


ARCHIVE_DIR = "_source_before_alignment"


def slug(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "slide"


def leading_number(path: Path) -> int | None:
    match = re.match(r"^(\d+)", path.stem)
    if not match:
        return None
    return int(match.group(1))


def clean_line(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip(" -\t")
    value = value.replace("➜", "->")
    value = value.replace("↔", "<->")
    return value


def slide_points(slide: Slide) -> list[str]:
    points: list[str] = []
    seen: set[str] = set()
    for raw in slide.text.splitlines():
        line = clean_line(raw)
        if not line:
            continue
        if line.lower() == clean_line(slide.title).lower():
            continue
        if line.startswith("Image:"):
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        points.append(line)
    return points[:6]


def sentence_from_points(points: list[str]) -> str:
    if not points:
        return "The slide frames the decision, evidence, or professional hand-off that learners need to recognise."
    if len(points) == 1:
        return points[0].rstrip(".") + "."
    if len(points) == 2:
        return f"{points[0].rstrip('.')}, and {points[1].rstrip('.')}."
    return f"{points[0].rstrip('.')}, {points[1].rstrip('.')}, and {points[2].rstrip('.')}."


def generated_narrative(topic: Topic, slide: Slide) -> str:
    points = slide_points(slide)
    first = sentence_from_points(points)
    if slide.n == 1:
        return (
            f"Speaker 1: This section sets up {topic.title}. Treat it as the frame for the decisions, "
            "handoffs, and evidence that appear in the next slides.\n"
            "Speaker 2: The practical question is simple: by the end, what should a junior IT professional "
            "be able to explain, check, or document in a real workplace?\n"
        )

    if slide.title.lower().startswith("key takeaway"):
        return (
            f"Speaker 1: The key takeaway is this: {first}\n"
            "Speaker 2: Use that takeaway to name the owner, evidence, and next action that should be visible after the work is done.\n"
        )

    detail = "; ".join(point.rstrip(".") for point in points[1:4])
    if detail:
        detail = f" Use the supporting details as a checklist: {detail}."
    return (
        f"Speaker 1: {slide.title} focuses attention on a concrete part of the work. {first}\n"
        f"Speaker 2: In practice, ask who owns the work, what evidence proves it happened, and what handoff comes next.{detail}\n"
    )


def is_old_generated(text: str) -> bool:
    markers = [
        "turns the topic into something observable",
        "This section introduces",
        "The detail to watch is",
        "The goal is not to memorise",
    ]
    return any(marker in text for marker in markers)


def map_existing_narratives(topic: Topic, files: list[Path]) -> dict[int, list[str]]:
    by_slide: dict[int, list[str]] = {}

    numeric = [(path, leading_number(path)) for path in files]
    if len(files) > len(topic.slides) and sum(n is not None for _, n in numeric) >= len(files) // 2:
        for path, number in numeric:
            text = path.read_text(encoding="utf-8")
            if number is None:
                continue
            target = min(max(number, 1), len(topic.slides))
            by_slide.setdefault(target, []).append(text.strip())
        return by_slide

    for mapping in align(topic):
        if mapping.slide is None:
            continue
        text = mapping.narrative.read_text(encoding="utf-8").strip()
        if text:
            by_slide.setdefault(mapping.slide.n, []).append(text)
    return by_slide


def archive_existing(narratives_dir: Path, files: list[Path]) -> None:
    archive = narratives_dir / ARCHIVE_DIR
    archive.mkdir(exist_ok=True)
    (archive / "README.md").write_text(
        "Original root-level narrative files preserved by `scripts/repair_narrative_alignment.py`.\n",
        encoding="utf-8",
    )
    for path in files:
        shutil.copy2(path, archive / path.name)
        path.unlink()


def repair_topic(topic: Topic) -> bool:
    files = narrative_files(topic.source_path)
    if len(files) == len(topic.slides):
        return False

    narratives_dir = topic.source_path / "narratives"
    narratives_dir.mkdir(exist_ok=True)
    by_slide = map_existing_narratives(topic, files)
    archive_existing(narratives_dir, files)

    for slide in topic.slides:
        chunks = [chunk for chunk in by_slide.get(slide.n, []) if chunk.strip()]
        if chunks:
            text = "\n\n".join(chunks).strip() + "\n"
        else:
            text = generated_narrative(topic, slide)
        name = f"{slide.n:02d}-{slug(slide.title)[:58]}.md"
        (narratives_dir / name).write_text(text, encoding="utf-8")
    return True


def main() -> None:
    if "--refresh-generated" in sys.argv:
        refreshed = 0
        for part in load_course():
            for topic in part.topics:
                for path in narrative_files(topic.source_path):
                    number = leading_number(path)
                    if number is None or number < 1 or number > len(topic.slides):
                        continue
                    text = path.read_text(encoding="utf-8")
                    if not is_old_generated(text):
                        continue
                    path.write_text(generated_narrative(topic, topic.slides[number - 1]), encoding="utf-8")
                    refreshed += 1
        print(f"Refreshed {refreshed} generated narrative files")
        return

    repaired: list[Path] = []
    for part in load_course():
        for topic in part.topics:
            if repair_topic(topic):
                repaired.append(topic.source_path.relative_to(ROOT))
    print(f"Repaired {len(repaired)} topics")
    for path in repaired:
        print(path)


if __name__ == "__main__":
    main()
