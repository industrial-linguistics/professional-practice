#!/usr/bin/env python3
"""Check narratives, slides, outlines and quizzes for generated filler and slop.

scripts/validate_textbook_sources.py already applies BANNED_PHRASES, but only
to content/**/textbook.md. Everything else a learner sees — the spoken
narration, the slides, the part blurbs that become the website — was never
checked, which is how 159 machine-generated narrative stubs reached the
repository and were recorded as audio.

This script covers those surfaces. Errors fail the run:

- generator stubs (scripts/repair_narrative_alignment.py leaves a TODO marker);
- the sentence templates that earlier versions of the generator emitted, which
  carried no marker and read as finished scripts.

There is deliberately no check for the run-together text that flattened tables
used to produce ("MIT/BSDAlmost anythingPreserve attribution"). Any pattern
loose enough to catch it also matches ordinary product names — TechCorp,
QuickBooks, JavaScript — and that failure mode is now fixed at source in
course_content.TextExtractor, with the marker above covering anything the
generator writes from here on.

Warnings do not fail unless --strict is given: banned slop phrases, US
spellings in a predominantly British/Australian body of text, and narration
long enough to overrun its slide.

Superseded drafts under narratives/_source_before_alignment/ are skipped.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from narrative_filler import find_generated_filler
from validate_textbook_sources import BANNED_PHRASES

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ARCHIVE_DIR = "_source_before_alignment"

# Phrases beyond the textbook list, each evidenced by a real hit in this repo.
EXTRA_BANNED_PHRASES = [
    "actionable insight",
    "force multiplier",
    "through an ethical lens",
    "plays a key role",
    "plays a crucial role",
    "game-changer",
    "game changer",
    "low-hanging fruit",
    "move the needle",
    "paradigm shift",
    "best-in-class",
    "unlock the potential",
    "harness the power",
    "at the end of the day",
    "in today's fast-paced world",
]

# US spellings whose British forms dominate this content (149 vs 26, and so on).
SPELLING = {
    "organiz": "organis",
    "prioritiz": "prioritis",
    "recogniz": "recognis",
    "optimiz": "optimis",
    "minimiz": "minimis",
    "standardiz": "standardis",
}

# Proper nouns that are spelled the way their source spells them. A book title
# and a maturity-model level are not ours to anglicise.
SPELLING_EXEMPT = [
    "Fearless Organization",  # Amy Edmondson's book
    "Optimized:",  # CMMI level 5, quoted from the model
]

# A slide runs about a minute, so narration much past that overruns it.
MAX_NARRATIVE_WORDS = 190


def narrative_files() -> list[Path]:
    return sorted(
        p
        for p in CONTENT.glob("part-*/*/narratives/*.md")
        if p.name != "outline.md" and ARCHIVE_DIR not in p.parts
    )


def other_files() -> list[Path]:
    paths = list(CONTENT.glob("part-*/*/slides.html"))
    paths += list(CONTENT.glob("part-*/outline.md"))
    paths += list(CONTENT.glob("part-*/quiz.md"))
    return sorted(p for p in paths if ARCHIVE_DIR not in p.parts)


def check_narrative(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)

    for reason in find_generated_filler(text):
        errors.append(f"{rel}: {reason}")

    words = len(re.findall(r"\S+", text))
    if words > MAX_NARRATIVE_WORDS:
        warnings.append(f"{rel}: {words} words; a slide runs about a minute (~100 words)")

    errors_, warnings_ = check_phrases(path, text)
    return errors + errors_, warnings + warnings_


def check_phrases(path: Path, text: str) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    rel = path.relative_to(ROOT)
    for i, line in enumerate(text.splitlines(), start=1):
        lower = line.lower()
        for phrase in list(BANNED_PHRASES) + EXTRA_BANNED_PHRASES:
            if phrase in lower:
                warnings.append(f"{rel}:{i}: slop phrase: {phrase!r}")
        if any(exempt in line for exempt in SPELLING_EXEMPT):
            continue
        for us, uk in SPELLING.items():
            if us in lower:
                warnings.append(f"{rel}:{i}: US spelling {us!r}; this content uses {uk!r}")
    return [], warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    narratives = narrative_files()
    for path in narratives:
        errs, warns = check_narrative(path)
        errors.extend(errs)
        warnings.extend(warns)

    others = other_files()
    for path in others:
        errs, warns = check_phrases(path, path.read_text(encoding="utf-8"))
        errors.extend(errs)
        warnings.extend(warns)

    for line in errors:
        print(f"ERROR {line}")
    for line in warnings:
        print(f"WARN  {line}")

    print(
        f"Checked {len(narratives)} narrative(s) and {len(others)} other source file(s): "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
