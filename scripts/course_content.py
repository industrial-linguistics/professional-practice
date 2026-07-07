#!/usr/bin/env python3
"""Shared course-content loading helpers for Professional Practice.

The editable slide source is HTML: one ``slides.html`` file per topic,
containing one ``<section class="slide">`` per learner-visible slide.
Narratives remain Markdown because the audio pipeline uses them directly.
"""

from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


@dataclass
class Slide:
    n: int
    title: str
    html: str
    text: str
    narration: str
    image_paths: list[str]


@dataclass
class Topic:
    part: str
    slug: str
    title: str
    summary: str
    source_path: Path
    slides: list[Slide]
    video: str | None
    audio: str | None
    subtitles: str | None

    @property
    def output_path(self) -> str:
        return f"{self.part}/{self.slug}/"


@dataclass
class Part:
    slug: str
    title: str
    summary: str
    topics: list[Topic]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in {"h1", "h2", "h3", "h4", "p", "li", "tr", "figcaption", "pre", "br"}:
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")
        if tag == "img":
            attr = dict(attrs)
            alt = attr.get("alt") or ""
            if alt:
                self.parts.append(f"Image: {alt}")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if not self.skip_depth and tag in {"h1", "h2", "h3", "h4", "p", "li", "tr", "pre"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        text = html.unescape("".join(self.parts))
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


class ImageExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.paths: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "img":
            return
        src = dict(attrs).get("src")
        if src:
            self.paths.append(src)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def titleize(slug: str) -> str:
    return " ".join(word.capitalize() for word in slug.replace("-", " ").split())


def html_to_text(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.text()


def image_paths(fragment: str) -> list[str]:
    parser = ImageExtractor()
    parser.feed(fragment)
    return parser.paths


def clean_slide_fragment(fragment: str) -> str:
    return re.sub(
        r"\s*<p\b[^>]*>\s*---\s*</p>\s*",
        "\n",
        fragment,
        flags=re.IGNORECASE,
    ).strip()


def summarize(text: str, limit: int = 190) -> str:
    text = re.sub(r"\bSpeaker\s+\d+:\s*", "", text)
    text = re.sub(r"\[[^\]]+\]\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "..."


def outline_info(part_dir: Path) -> tuple[str, str]:
    outline = part_dir / "outline.md"
    fallback = titleize(part_dir.name)
    if not outline.exists():
        return fallback, ""
    lines = read_text(outline).splitlines()
    title = fallback
    summary = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            title = re.sub(
                r"^#\s*Part\s+\d+\s*[-\u2013\u2014]\s*",
                "",
                stripped,
                flags=re.IGNORECASE,
            ).strip("# ")
            continue
        summary = summarize(stripped)
        break
    return title or fallback, summary


def narrative_files(topic_dir: Path) -> list[Path]:
    narratives = topic_dir / "narratives"
    if not narratives.exists():
        return []
    return sorted(
        p
        for p in narratives.glob("*.md")
        if p.is_file() and p.name.lower() not in {"outline.md", "readme.md"}
    )


def copy_if_exists(src: Path, dest_dir: Path) -> str | None:
    if not src.exists():
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    return dest.name


def topic_audio_filename(topic_dir: Path) -> str | None:
    if (topic_dir / "audio.mp3").exists():
        return "audio.mp3"
    if (topic_dir / "audio.wav").exists():
        return "audio.wav"
    return None


def section_fragments(slides_html: str) -> list[str]:
    pattern = re.compile(
        r"(<section\b(?=[^>]*\bclass=[\"'][^\"']*\bslide\b)[^>]*>.*?</section>)",
        re.IGNORECASE | re.DOTALL,
    )
    return [match.group(1).strip() for match in pattern.finditer(slides_html)]


def attr_value(tag: str, name: str) -> str | None:
    match = re.search(
        rf"\b{name}\s*=\s*([\"'])(.*?)\1",
        tag,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    return html.unescape(match.group(2))


def slide_title(fragment: str, fallback: str) -> str:
    start = fragment.split(">", 1)[0]
    data_title = attr_value(start, "data-title")
    if data_title:
        return data_title
    heading = re.search(r"<h[1-4]\b[^>]*>(.*?)</h[1-4]>", fragment, re.IGNORECASE | re.DOTALL)
    if heading:
        text = html_to_text(heading.group(1))
        if text:
            return text
    text = html_to_text(fragment)
    return summarize(text, 80) or fallback


def load_topic(part_slug: str, topic_dir: Path) -> Topic:
    slides_path = topic_dir / "slides.html"
    fragments = section_fragments(read_text(slides_path))
    narratives = [read_text(path) for path in narrative_files(topic_dir)]
    narrative_texts = [markdown_to_plain(text) for text in narratives]

    slides: list[Slide] = []
    for i, fragment in enumerate(fragments):
        fragment = clean_slide_fragment(fragment)
        title = slide_title(fragment, f"Slide {i + 1}")
        slides.append(
            Slide(
                n=i + 1,
                title=title,
                html=fragment,
                text=html_to_text(fragment),
                narration=narrative_texts[i] if i < len(narrative_texts) else "",
                image_paths=image_paths(fragment),
            )
        )

    title = slides[0].title if slides else titleize(topic_dir.name)
    summary = ""
    if narrative_texts:
        summary = summarize(narrative_texts[0])
    elif slides:
        summary = summarize(slides[0].text)

    return Topic(
        part=part_slug,
        slug=topic_dir.name,
        title=title,
        summary=summary,
        source_path=topic_dir,
        slides=slides,
        video="final.mp4" if (topic_dir / "final.mp4").exists() else None,
        audio=topic_audio_filename(topic_dir),
        subtitles="subtitles.vtt" if (topic_dir / "subtitles.vtt").exists() else None,
    )


def load_course(content_dir: Path = CONTENT) -> list[Part]:
    parts: list[Part] = []
    for part_dir in sorted(content_dir.glob("part-*")):
        if not part_dir.is_dir():
            continue
        title, summary = outline_info(part_dir)
        topics = [
            load_topic(part_dir.name, topic_dir)
            for topic_dir in sorted(part_dir.iterdir())
            if topic_dir.is_dir() and (topic_dir / "slides.html").exists()
        ]
        parts.append(Part(part_dir.name, title, summary, topics))
    return parts


def markdown_to_plain(markdown: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"Image: \1", markdown)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^[#>*\-\s]+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def copy_topic_images(topic: Topic, out_dir: Path) -> None:
    images = topic.source_path / "images"
    if not images.exists():
        return
    dest = out_dir / "images"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(images, dest)


def rewrite_image_paths(fragment: str, prefix: str) -> str:
    escaped_prefix = html.escape(prefix.rstrip("/") + "/", quote=True)
    fragment = re.sub(r'src="images/', f'src="{escaped_prefix}images/', fragment)
    fragment = re.sub(r"src='images/", f"src='{escaped_prefix}images/", fragment)
    return fragment
