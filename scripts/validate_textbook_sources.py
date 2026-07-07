#!/usr/bin/env python3
"""Validate authored textbook.md sources against the markdown-subset contract.

See docs/textbook-authoring-guidelines.md. Exits non-zero on errors;
warnings (length, missing files) are reported but do not fail the run
unless --strict is given.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

BANNED_PHRASES = [
    "in today's fast-paced",
    "fast-paced world",
    "more important than ever",
    "ever-evolving",
    "in conclusion",
    "let's delve",
    "delve into",
    "in the landscape of",
    "navigating the landscape",
]

MIN_WORDS = 600
MAX_WORDS = 2600


def topic_dirs() -> list[Path]:
    return sorted(p.parent for p in CONTENT.glob("part-*/*/slides.html"))


def check_file(path: Path, *, is_intro: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)

    in_code = False
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^#\s", stripped):
            errors.append(f"{rel}:{i}: top-level '#' heading (the generator emits the title)")
        if stripped.startswith("|"):
            errors.append(f"{rel}:{i}: table syntax is not supported")
        if re.search(r"<[a-zA-Z][^>]*>", stripped):
            errors.append(f"{rel}:{i}: raw HTML is not supported")
        for match in re.finditer(r"(!?)\[[^\]]*\]\(([^)]+)\)", stripped):
            bang, target = match.groups()
            if not bang:
                errors.append(f"{rel}:{i}: links are not supported (print-first book)")
            else:
                img = path.parent / target
                if re.match(r"^[a-z]+:", target) or target.startswith("/"):
                    errors.append(f"{rel}:{i}: image path must be topic-relative: {target}")
                elif not img.exists():
                    errors.append(f"{rel}:{i}: image does not exist: {target}")
        lower = stripped.lower()
        for phrase in BANNED_PHRASES:
            if phrase in lower:
                warnings.append(f"{rel}:{i}: slop phrase: {phrase!r}")

    if in_code:
        errors.append(f"{rel}: unclosed code fence")

    words = len(re.findall(r"\S+", text))
    if not is_intro:
        if words < MIN_WORDS:
            warnings.append(f"{rel}: only {words} words (guideline minimum ~900)")
        elif words > MAX_WORDS:
            warnings.append(f"{rel}: {words} words (guideline maximum ~1800)")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    missing: list[str] = []
    authored = 0

    for topic in topic_dirs():
        source = topic / "textbook.md"
        if not source.exists():
            missing.append(str(source.relative_to(ROOT)))
            continue
        authored += 1
        errs, warns = check_file(source)
        errors.extend(errs)
        warnings.extend(warns)

    for intro in sorted(CONTENT.glob("part-*/textbook-intro.md")):
        errs, warns = check_file(intro, is_intro=True)
        errors.extend(errs)
        warnings.extend(warns)

    for line in errors:
        print(f"ERROR {line}")
    for line in warnings:
        print(f"WARN  {line}")
    if missing:
        print(f"Missing textbook.md for {len(missing)} topic(s):")
        for line in missing:
            print(f"  - {line}")

    total = len(topic_dirs())
    print(f"Checked {authored}/{total} authored topics: {len(errors)} error(s), {len(warnings)} warning(s)")
    if errors or (args.strict and (warnings or missing)):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
