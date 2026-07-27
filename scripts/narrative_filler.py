#!/usr/bin/env python3
"""Detect machine-generated filler in narration.

Narration is read aloud by the TTS pipeline, so an unfinished generated stub
that reaches a build gets recorded and shipped. This module is the single
source of truth for what generated filler looks like, so every entry point
that can trigger generation — the repo-wide validator, the per-topic
pre-generation gate, and the e-learning build — agrees on the answer.

Kept dependency-free on purpose: scripts/validate_content.py runs once per
topic in a shell loop and should not pull in the course loader to do it.
"""

from __future__ import annotations

# Written by scripts/repair_narrative_alignment.py into every narrative it
# generates. Its presence means "nobody has written this yet".
STUB_MARKER = "<!-- TODO(narrative): generated stub, rewrite before recording -->"

# Sentence frames emitted by earlier versions of generated_narrative(). These
# carry no marker and read as finished scripts, which is exactly why 159 of
# them were recorded as audio before anyone noticed. Matched by their text.
GENERATOR_TEMPLATES = [
    "focuses attention on a concrete part of the work",
    "In practice, ask who owns the work, what evidence proves it happened",
    "Use the supporting details as a checklist",
    "This section sets up",
    "The practical question is simple: by the end, what should a junior IT professional",
    "The key takeaway is this:",
    "Use that takeaway to name the owner, evidence, and next action",
    "turns the topic into something observable",
    "The detail to watch is",
    "The goal is not to memorise",
]


def find_generated_filler(text: str) -> list[str]:
    """Return reasons this narration looks generated. Empty means it is fine."""
    if STUB_MARKER in text:
        return ["unwritten generator stub; write the narration before recording"]
    return [f"generated filler: {template!r}" for template in GENERATOR_TEMPLATES if template in text]
