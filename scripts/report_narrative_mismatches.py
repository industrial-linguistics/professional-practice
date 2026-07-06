#!/usr/bin/env python3
"""Write a slide/narrative mismatch audit for the HTML course source."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from course_content import ROOT, Slide, Topic, load_course, markdown_to_plain, narrative_files


REPORT = ROOT / "docs" / "narrative-mismatch-audit.md"

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "vs",
    "with",
}


@dataclass
class Mapping:
    narrative: Path
    slide: Slide | None
    score: int


def md_escape(value: str) -> str:
    return value.replace("|", r"\|")


def tokens(value: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", value.lower())
    return {word for word in words if len(word) > 1 and word not in STOPWORDS}


def narrative_label(path: Path) -> str:
    stem = re.sub(r"^\d+[-_]*", "", path.stem)
    return stem.replace("-", " ")


def is_title_slide(slide: Slide) -> bool:
    start = slide.html.split(">", 1)[0].lower()
    return 'data-kind="title"' in start or "data-kind='title'" in start


def score_pair(narrative_path: Path, narrative_text: str, slide: Slide, slide_index: int) -> int:
    label_tokens = tokens(narrative_label(narrative_path))
    narrative_tokens = tokens(narrative_text)
    slide_title_tokens = tokens(slide.title)
    slide_text_tokens = tokens(slide.text)
    score = 0
    score += 4 * len(label_tokens & slide_title_tokens)
    score += 2 * len(label_tokens & slide_text_tokens)
    score += len(narrative_tokens & slide_title_tokens)
    score += len(narrative_tokens & slide_text_tokens)
    if slide_index == 0 and is_title_slide(slide):
        if label_tokens & {"intro", "introduction", "overview", "welcome", "opening", "title"}:
            score += 8
    return score


def align(topic: Topic) -> list[Mapping]:
    files = narrative_files(topic.source_path)
    narrative_texts = [
        markdown_to_plain(path.read_text(encoding="utf-8", errors="replace")) for path in files
    ]
    mappings: list[Mapping] = []
    cursor = 0
    for path, text in zip(files, narrative_texts):
        if cursor >= len(topic.slides):
            mappings.append(Mapping(path, None, 0))
            continue
        scored: list[tuple[int, int, Slide]] = []
        for index in range(cursor, len(topic.slides)):
            slide = topic.slides[index]
            scored.append((score_pair(path, text, slide, index), index, slide))
        score, index, slide = max(scored, key=lambda item: (item[0], -item[1]))
        if score == 0:
            index = cursor
            slide = topic.slides[index]
        mappings.append(Mapping(path, slide, score))
        cursor = index + 1
    return mappings


def classify(topic: Topic, narrative_count: int) -> str:
    slide_count = len(topic.slides)
    first_is_title = bool(topic.slides and is_title_slide(topic.slides[0]))
    if narrative_count == 0:
        return "no narratives"
    if narrative_count > slide_count:
        return "extra narratives"
    if slide_count == narrative_count + 1 and first_is_title:
        return "one-slide gap with title slide"
    if slide_count > narrative_count and first_is_title:
        return "multi-slide gap with title slide"
    if slide_count > narrative_count:
        return "partial gap"
    return "matched"


def uncovered_slides(topic: Topic, mappings: list[Mapping]) -> list[Slide]:
    covered = {mapping.slide.n for mapping in mappings if mapping.slide is not None}
    return [slide for slide in topic.slides if slide.n not in covered]


def render() -> str:
    parts = load_course()
    topics = [topic for part in parts for topic in part.topics]
    rows: list[str] = []
    detail: list[str] = []
    counts: dict[str, int] = {}
    mismatch_count = 0

    for topic in topics:
        files = narrative_files(topic.source_path)
        kind = classify(topic, len(files))
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "matched":
            continue
        mismatch_count += 1
        mappings = align(topic)
        missing = uncovered_slides(topic, mappings)
        missing_text = "; ".join(f"{slide.n}. {slide.title}" for slide in missing) or "none detected"
        rows.append(
            "| {path} | {slides} | {narratives} | {kind} | {missing} |".format(
                path=md_escape(str(topic.source_path.relative_to(ROOT))),
                slides=len(topic.slides),
                narratives=len(files),
                kind=kind,
                missing=md_escape(missing_text),
            )
        )
        detail.append(f"### {topic.source_path.relative_to(ROOT)}\n")
        detail.append(f"- Slides: {len(topic.slides)}")
        detail.append(f"- Narratives: {len(files)}")
        detail.append(f"- Classification: {kind}")
        detail.append(f"- Candidate uncovered slides: {missing_text or 'none detected'}")
        if any(mapping.score for mapping in mappings):
            detail.append("- Heuristic narrative mapping:")
            for mapping in mappings:
                target = (
                    f"slide {mapping.slide.n}: {mapping.slide.title}"
                    if mapping.slide is not None
                    else "no slide"
                )
                detail.append(
                    f"  - `{mapping.narrative.name}` -> {target} (score {mapping.score})"
                )
        detail.append("")

    summary_lines = [
        "# Narrative Mismatch Audit",
        "",
        "Generated by `scripts/report_narrative_mismatches.py`.",
        "",
        f"- Topics: {len(topics)}",
        f"- Mismatched topics: {mismatch_count}",
        f"- Matched topics: {counts.get('matched', 0)}",
    ]
    for kind in sorted(k for k in counts if k != "matched"):
        summary_lines.append(f"- {kind}: {counts[kind]}")
    summary_lines.extend(
        [
            "",
            "The candidate uncovered slide list is a deterministic heuristic based on narrative filenames, narrative text, slide titles, and slide text. Treat it as a triage queue, not an approval decision.",
            "",
            "| Topic | Slides | Narratives | Classification | Candidate uncovered slides |",
            "| --- | ---: | ---: | --- | --- |",
        ]
    )
    summary_lines.extend(rows)
    summary_lines.extend(["", "## Detail", ""])
    summary_lines.extend(detail)
    return "\n".join(summary_lines).rstrip() + "\n"


def main() -> None:
    REPORT.write_text(render(), encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
