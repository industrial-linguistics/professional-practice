#!/usr/bin/env python3
"""Validate the HTML-source course and generated learner outputs."""

from __future__ import annotations

import argparse
import base64
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from course_content import CONTENT, ROOT, load_course, narrative_files


@dataclass
class Issue:
    path: Path
    message: str


class LocalAssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag in {"a", "link"} and attr.get("href"):
            self.refs.append(("href", attr["href"] or ""))
        if tag in {"img", "script", "source", "video", "audio"} and attr.get("src"):
            self.refs.append(("src", attr["src"] or ""))


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.bad_nested_lists = 0
        self.sections = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "section" and "slide" in (attr.get("class") or "").split():
            self.sections += 1
        if tag in {"ul", "ol"} and self.stack and self.stack[-1] in {"ul", "ol"}:
            self.bad_nested_lists += 1
        self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                del self.stack[i:]
                return


def source_topics() -> list[Path]:
    return sorted(path.parent for path in CONTENT.glob("part-*/*/slides.html"))


def validate_source() -> list[Issue]:
    issues: list[Issue] = []
    warnings: list[str] = []
    legacy = sorted(CONTENT.glob("part-*/*/slides.md"))
    for path in legacy:
        issues.append(Issue(path, "legacy slides.md remains after HTML migration"))
    parts = load_course()
    if not parts:
        issues.append(Issue(CONTENT, "no course parts found"))
    topic_total = 0
    slide_total = 0
    for part in parts:
        for topic in part.topics:
            topic_total += 1
            slide_total += len(topic.slides)
            if not topic.slides:
                issues.append(Issue(topic.source_path / "slides.html", "no slide sections found"))
            narratives = narrative_files(topic.source_path)
            if len(narratives) != len(topic.slides):
                warnings.append(
                    f"{topic.source_path.relative_to(ROOT)}: "
                    f"{len(topic.slides)} slides, {len(narratives)} narratives"
                )
            parser = StructureParser()
            parser.feed((topic.source_path / "slides.html").read_text(encoding="utf-8"))
            if parser.bad_nested_lists:
                issues.append(Issue(topic.source_path / "slides.html", "malformed nested list structure"))
            for slide in topic.slides:
                if not slide.title:
                    issues.append(Issue(topic.source_path / "slides.html", f"slide {slide.n} has no title"))
                if not slide.text and not slide.image_paths:
                    issues.append(Issue(topic.source_path / "slides.html", f"slide {slide.n} has no visible text or image"))
                for src in slide.image_paths:
                    if re.match(r"^[a-z]+:", src) or src.startswith(("/", "#")):
                        continue
                    candidate = topic.source_path / src
                    if not candidate.exists():
                        issues.append(Issue(candidate, f"missing image referenced by slide {slide.n}"))
    if topic_total == 0:
        issues.append(Issue(CONTENT, "no topics with slides.html found"))
    print(f"Validated source: {topic_total} topics, {slide_total} slides")
    if warnings:
        print(f"Warnings: {len(warnings)} slide/narrative count mismatches")
        for warning in warnings[:12]:
            print(f"- {warning}")
        if len(warnings) > 12:
            print(f"- ... {len(warnings) - 12} more")
    return issues


def is_external(ref: str) -> bool:
    return (
        not ref
        or ref.startswith("#")
        or ref.startswith("mailto:")
        or ref.startswith("data:")
        or ref.startswith("http://")
        or ref.startswith("https://")
        or ref.startswith("javascript:")
    )


def validate_generated_links(base: Path) -> list[Issue]:
    issues: list[Issue] = []
    if not base.exists():
        issues.append(Issue(base, "generated output directory not found"))
        return issues
    for html_path in sorted(base.rglob("*.html")):
        parser = LocalAssetParser()
        parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))
        for attr, ref in parser.refs:
            if is_external(ref):
                continue
            clean_ref = ref.split("#", 1)[0].split("?", 1)[0]
            if not clean_ref:
                continue
            target = (html_path.parent / clean_ref).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                issues.append(Issue(html_path, f"{attr} escapes repo: {ref}"))
                continue
            if not target.exists():
                issues.append(Issue(html_path, f"missing {attr} target: {ref}"))
    print(f"Validated generated links under {base.relative_to(ROOT)}")
    return issues


def validate_generated_artifacts() -> list[Issue]:
    issues: list[Issue] = []
    artifacts = [
        ROOT / "textbook" / "main.pdf",
        ROOT / "textbook" / "main-amazon.pdf",
        ROOT / "output" / "site" / "textbook" / "main.pdf",
        ROOT / "output" / "elearning" / "textbook" / "main.pdf",
    ]
    for artifact in artifacts:
        if not artifact.exists():
            issues.append(Issue(artifact, "expected generated PDF artifact is missing"))
        elif artifact.stat().st_size < 100_000:
            issues.append(Issue(artifact, "generated PDF artifact is unexpectedly small"))
    if not issues:
        print("Validated generated textbook PDF artifacts")
    return issues


def read_secret(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value
    return data


def http_status(url: str, username: str | None = None, password: str | None = None) -> int:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "professional-practice-course-smoke/1.0"},
    )
    if username is not None and password is not None:
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        request.add_header("Authorization", f"Basic {token}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


def validate_auth(secret_file: Path) -> list[Issue]:
    issues: list[Issue] = []
    secret = read_secret(secret_file)
    required = {"URL", "USERNAME", "PASSWORD"}
    if not required.issubset(secret):
        issues.append(Issue(secret_file, "auth secret missing URL, USERNAME or PASSWORD"))
        return issues
    noauth = http_status(secret["URL"])
    auth = http_status(secret["URL"], secret["USERNAME"], secret["PASSWORD"])
    if noauth != 401:
        issues.append(Issue(secret_file, f"expected unauthenticated 401, got {noauth}"))
    if auth != 200:
        issues.append(Issue(secret_file, f"expected authenticated 200, got {auth}"))
    print(f"Validated protected review URL: unauth={noauth}, auth={auth}")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--auth-smoke", action="store_true")
    parser.add_argument(
        "--secret-file",
        type=Path,
        default=ROOT / "state" / "secrets" / "image-review-basic-auth.env",
    )
    args = parser.parse_args()

    issues = validate_source()
    if args.check_output:
        issues.extend(validate_generated_links(ROOT / "output" / "elearning"))
        issues.extend(validate_generated_links(ROOT / "output" / "site"))
        issues.extend(validate_generated_links(ROOT / "textbook"))
        issues.extend(validate_generated_artifacts())
    if args.auth_smoke:
        issues.extend(validate_auth(args.secret_file))

    if issues:
        print("\nValidation failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue.path}: {issue.message}", file=sys.stderr)
        raise SystemExit(1)
    print("HTML course validation passed")


if __name__ == "__main__":
    main()
