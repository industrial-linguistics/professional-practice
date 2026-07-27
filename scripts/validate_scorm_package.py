#!/usr/bin/env python3
"""Validate the saleable IT Professional Practice SCORM 1.2 package."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from html import unescape
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from course_content import ROOT


DEFAULT_PACKAGE = (
    ROOT / "output" / "scorm" / "it-professional-practice-incident-triage.zip"
)
SCORM_NAMESPACE = "http://www.adlnet.org/xsd/adlcp_rootv1p2"
EXPECTED_LESSONS = 7
EXPECTED_SLIDES = 34
EXPECTED_SCENARIOS = 5
EXPECTED_DECISIONS = 20
EXPECTED_AUDIO = 7
PASS_SCORE = "70"


def normalized_names(archive: ZipFile) -> set[str]:
    return {
        str(PurePosixPath(name.removeprefix("./")))
        for name in archive.namelist()
        if not name.endswith("/")
    }


def elements_ending_in(root: ElementTree.Element, local_name: str):
    return [
        element
        for element in root.iter()
        if element.tag == local_name or element.tag.endswith(f"}}{local_name}")
    ]


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        archive = ZipFile(path)
    except (FileNotFoundError, BadZipFile) as exc:
        return [str(exc)]

    with archive:
        corrupt = archive.testzip()
        if corrupt:
            errors.append(f"corrupt ZIP member: {corrupt}")
        names = normalized_names(archive)
        if "imsmanifest.xml" not in names:
            return errors + ["imsmanifest.xml is missing from the package root"]
        try:
            manifest = ElementTree.fromstring(archive.read("imsmanifest.xml"))
        except ElementTree.ParseError as exc:
            return errors + [f"imsmanifest.xml is invalid XML: {exc}"]

        versions = [
            (element.text or "").strip()
            for element in elements_ending_in(manifest, "schemaversion")
        ]
        if versions != ["1.2"]:
            errors.append(f"expected SCORM 1.2, found {versions!r}")

        resources = elements_ending_in(manifest, "resource")
        sco_resources = [
            resource
            for resource in resources
            if resource.attrib.get(f"{{{SCORM_NAMESPACE}}}scormtype") == "sco"
        ]
        if len(sco_resources) != 1:
            errors.append(f"expected one SCO resource, found {len(sco_resources)}")
        elif sco_resources[0].attrib.get("href") != "index.html":
            errors.append("the SCO must launch index.html")

        mastery_scores = [
            (element.text or "").strip()
            for element in elements_ending_in(manifest, "masteryscore")
        ]
        if mastery_scores != [PASS_SCORE]:
            errors.append(
                f"expected mastery score {PASS_SCORE}, found {mastery_scores!r}"
            )

        declared = {
            element.attrib.get("href", "")
            for element in elements_ending_in(manifest, "file")
        }
        actual_content = names - {"imsmanifest.xml"}
        missing = sorted(declared - actual_content)
        undeclared = sorted(actual_content - declared)
        if missing:
            errors.append(f"manifest references {len(missing)} missing file(s)")
        if undeclared:
            errors.append(f"manifest omits {len(undeclared)} package file(s)")

        required = {
            "index.html",
            "incident-triage.html",
            "course-corpus.json",
            "assets/course.css",
            "assets/course.js",
            "assets/module.css",
            "assets/scorm-runtime.js",
            "assets/incident-triage.js",
            "assets/scenarios.json",
            "resources/intake-and-escalation-sheet.html",
            "resources/facilitator-guide.html",
        }
        for name in sorted(required - names):
            errors.append(f"required package file missing: {name}")

        for page_name in sorted(name for name in names if name.endswith(".html")):
            page = archive.read(page_name).decode("utf-8")
            for raw_href in re.findall(r'\bhref="([^"]+)"', page):
                href = unescape(raw_href)
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or href.startswith(("#", "/")):
                    continue
                local_path = unquote(parsed.path)
                if not local_path:
                    continue
                if local_path.endswith("/"):
                    errors.append(
                        f"{page_name}: local link must name an explicit file: {href}"
                    )
                    continue
                target = posixpath.normpath(
                    posixpath.join(posixpath.dirname(page_name), local_path)
                )
                if target not in names:
                    errors.append(
                        f"{page_name}: local link target is missing: {href}"
                    )

        lesson_pages = sorted(
            name
            for name in names
            if re.fullmatch(r"part-01/[^/]+/index\.html", name)
        )
        if len(lesson_pages) != EXPECTED_LESSONS:
            errors.append(
                f"expected {EXPECTED_LESSONS} lesson pages, found {len(lesson_pages)}"
            )

        slide_count = 0
        for lesson_page in lesson_pages:
            page = archive.read(lesson_page).decode("utf-8")
            match = re.search(
                r'<script id="lesson-data" type="application/json">(.*?)</script>',
                page,
                re.DOTALL,
            )
            if not match:
                errors.append(f"{lesson_page}: lesson-data is missing")
                continue
            try:
                payload = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"{lesson_page}: invalid lesson-data JSON: {exc}")
                continue
            slide_count += len(payload.get("slides", []))
            if 'data-scorm-page="lesson"' not in page:
                errors.append(f"{lesson_page}: SCORM lesson marker is missing")
            if "../../assets/scorm-runtime.js" not in page:
                errors.append(f"{lesson_page}: SCORM runtime is not loaded")
        if slide_count != EXPECTED_SLIDES:
            errors.append(
                f"expected {EXPECTED_SLIDES} learner slides, found {slide_count}"
            )

        audio_files = [name for name in names if name.endswith("/audio.mp3")]
        if len(audio_files) != EXPECTED_AUDIO:
            errors.append(
                f"expected {EXPECTED_AUDIO} narrated lesson files, found {len(audio_files)}"
            )

        transcript_texts = [
            name for name in names if name.endswith("/transcript.txt")
        ]
        if len(transcript_texts) != EXPECTED_LESSONS:
            errors.append(
                f"expected {EXPECTED_LESSONS} plain transcripts, "
                f"found {len(transcript_texts)}"
            )

        if "assets/scenarios.json" in names:
            scenarios = json.loads(
                archive.read("assets/scenarios.json").decode("utf-8")
            ).get("scenarios", [])
            decisions = sum(len(item.get("decisions", [])) for item in scenarios)
            if len(scenarios) != EXPECTED_SCENARIOS:
                errors.append(
                    f"expected {EXPECTED_SCENARIOS} scenarios, found {len(scenarios)}"
                )
            if decisions != EXPECTED_DECISIONS:
                errors.append(
                    f"expected {EXPECTED_DECISIONS} scored decisions, found {decisions}"
                )

        if "assets/scorm-runtime.js" in names:
            runtime = archive.read("assets/scorm-runtime.js").decode("utf-8")
            required_calls = {
                "LMSInitialize",
                "LMSGetValue",
                "LMSSetValue",
                "LMSCommit",
                "LMSFinish",
                "cmi.core.lesson_status",
                "cmi.core.lesson_location",
                "cmi.core.score.raw",
                "cmi.suspend_data",
                "cmi.core.exit",
            }
            for call in sorted(required_calls):
                if call not in runtime:
                    errors.append(f"SCORM runtime does not reference {call}")

        if "assets/course.js" in names:
            course_runtime = archive.read("assets/course.js").decode("utf-8")
            if re.search(r"^\s*maybeEnableLocalQa\(\);\s*$", course_runtime, re.MULTILINE):
                errors.append(
                    "portable course runtime still starts local browser-model Q&A"
                )

        if "index.html" in names:
            hub = archive.read("index.html").decode("utf-8")
            required_copy = [
                "Make defensible first-call decisions.",
                "Incident Triage Lab",
                "AI-generated voice",
                "not accredited by or affiliated with PeopleCert",
            ]
            for text in required_copy:
                if text not in hub:
                    errors.append(f"module home is missing required copy: {text}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?", type=Path, default=DEFAULT_PACKAGE)
    args = parser.parse_args()
    errors = validate(args.archive)
    if errors:
        print(f"SCORM validation failed for {args.archive}:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(
        f"SCORM validation passed: {args.archive} "
        f"({EXPECTED_LESSONS} lessons, {EXPECTED_SLIDES} slides, "
        f"{EXPECTED_SCENARIOS} scenarios, {EXPECTED_AUDIO} audio files)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
