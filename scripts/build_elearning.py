#!/usr/bin/env python3
"""Build the learner-facing e-learning surface from HTML slide source."""

from __future__ import annotations

import html
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from course_content import (
    ROOT,
    Part,
    Topic,
    copy_if_exists,
    copy_topic_images,
    load_course,
    titleize,
)


OUTPUT = ROOT / "output"
ELEARNING = OUTPUT / "elearning"
SITE = OUTPUT / "site"
TEXTBOOK = ROOT / "textbook"
PUBLISHED_TEXTBOOK_FILES = [
    ("main.pdf", "Student A4 PDF"),
]
AUDIO_MP3_BITRATE = os.environ.get("AUDIO_MP3_BITRATE", "96k")
SPEAKER_DISPLAY_NAMES = {
    "Speaker 1": "Anna",
    "Speaker 2": "Greg",
}
VTT_TIMESTAMP_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}:\d{2}\.\d{3})"
)


def clean_output() -> None:
    if ELEARNING.exists():
        shutil.rmtree(ELEARNING)
    if SITE.exists():
        shutil.rmtree(SITE)
    (ELEARNING / "assets").mkdir(parents=True, exist_ok=True)
    (ELEARNING / "media").mkdir(parents=True, exist_ok=True)
    SITE.mkdir(parents=True, exist_ok=True)


def json_for_script(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def asset_version() -> str:
    return hashlib.sha256((COURSE_CSS + COURSE_JS).encode("utf-8")).hexdigest()[:12]


def write_assets() -> None:
    (ELEARNING / "assets" / "course.css").write_text(COURSE_CSS, encoding="utf-8")
    (ELEARNING / "assets" / "course.js").write_text(COURSE_JS, encoding="utf-8")


def transcode_wav_to_mp3(src: Path, dest: Path) -> str:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError(
            f"ffmpeg is required to publish compressed audio for {src.relative_to(ROOT)}"
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            AUDIO_MP3_BITRATE,
            str(dest),
        ],
        check=True,
    )
    return dest.name


def publish_audio(src_dir: Path, media_dir: Path) -> str | None:
    source_mp3 = src_dir / "audio.mp3"
    if source_mp3.exists():
        return copy_if_exists(source_mp3, media_dir)

    source_wav = src_dir / "audio.wav"
    if source_wav.exists():
        return transcode_wav_to_mp3(source_wav, media_dir / "audio.mp3")

    return None


def audio_mime(filename: str) -> str:
    if filename.lower().endswith(".mp3"):
        return "audio/mpeg"
    return "audio/wav"


def copy_topic_media(topic: Topic) -> tuple[str | None, str | None]:
    media_dir = ELEARNING / "media" / topic.part / topic.slug
    audio = publish_audio(topic.source_path, media_dir)
    subtitles = copy_if_exists(topic.source_path / "subtitles.vtt", media_dir)
    return audio, subtitles


def vtt_seconds(timestamp: str) -> float:
    hours, minutes, seconds = timestamp.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def slide_timings(topic: Topic) -> list[dict[str, float | int]]:
    vtt_path = topic.source_path / "subtitles.vtt"
    if not vtt_path.exists():
        return []

    timings: dict[int, dict[str, float | int]] = {}
    lines = vtt_path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        match = VTT_TIMESTAMP_RE.search(line)
        if not match:
            continue
        cue_id = lines[i - 1].strip() if i > 0 else ""
        cue_match = re.match(r"^(\d+)(?:\.\d+)?$", cue_id)
        if not cue_match:
            continue
        index = int(cue_match.group(1)) - 1
        if index < 0:
            continue
        start = vtt_seconds(match.group("start"))
        end = vtt_seconds(match.group("end"))
        existing = timings.get(index)
        if existing is None:
            timings[index] = {"index": index, "start": start, "end": end}
        else:
            existing["start"] = min(float(existing["start"]), start)
            existing["end"] = max(float(existing["end"]), end)

    return [timings[i] for i in sorted(timings)]


def display_narration(text: str) -> str:
    for source, display in SPEAKER_DISPLAY_NAMES.items():
        text = re.sub(
            rf"(?m)^\s*{re.escape(source)}\s*:",
            f"{display}:",
            text,
        )
    return text


def next_topic_payload(topic: Topic, next_topic: Topic | None) -> dict | None:
    if next_topic is None:
        return None
    current_dir = ELEARNING / topic.part / topic.slug
    next_dir = ELEARNING / next_topic.part / next_topic.slug
    href = os.path.relpath(next_dir, current_dir).replace(os.sep, "/")
    if not href.endswith("/"):
        href += "/"
    return {
        "title": next_topic.title,
        "href": href,
        "part": titleize(next_topic.part),
    }


def lesson_payload(
    topic: Topic,
    media_base: str,
    audio: str | None,
    subtitles: str | None,
    next_topic: Topic | None,
) -> dict:
    return {
        "topicPath": f"{topic.part}/{topic.slug}",
        "title": topic.title,
        "summary": topic.summary,
        "mediaBase": media_base,
        "audio": audio,
        "subtitles": subtitles,
        "nextTopic": next_topic_payload(topic, next_topic),
        "slideTimings": slide_timings(topic),
        "slides": [
            {
                "n": slide.n,
                "title": slide.title,
                "html": slide.html,
                "text": slide.text,
                "narration": display_narration(slide.narration),
            }
            for slide in topic.slides
        ],
    }


def render_topic(topic: Topic, next_topic: Topic | None = None) -> None:
    out_dir = ELEARNING / topic.part / topic.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    copy_topic_images(topic, out_dir)
    rel_media = f"../../media/{topic.part}/{topic.slug}"
    audio, subtitles = copy_topic_media(topic)
    data = lesson_payload(topic, rel_media, audio, subtitles, next_topic)
    slide_buttons = "\n".join(
        f'<button type="button" class="slide-jump" data-slide="{slide.n - 1}">'
        f'<span>{slide.n:02d}</span>{html.escape(slide.title)}</button>'
        for slide in topic.slides
    )
    audio_block = (
        '<audio id="audio-player" controls preload="metadata">'
        f'<source src="{rel_media}/{audio}" type="{audio_mime(audio)}">'
        "</audio>"
        if audio
        else '<span class="pending">Audio pending</span>'
    )
    subtitles_link = (
        f'<a href="{rel_media}/{subtitles}">Download subtitles</a>'
        if subtitles
        else '<span class="pending">Subtitles pending</span>'
    )
    next_topic = data.get("nextTopic")
    next_topic_button = (
        '<a id="next-topic" class="next-topic-button" '
        f'href="{html.escape(str(next_topic["href"]), quote=True)}" hidden>'
        f'Next topic: <span>{html.escape(str(next_topic["title"]))}</span></a>'
        if next_topic
        else ""
    )
    html_text = TOPIC_PAGE.format(
        title=html.escape(topic.title),
        summary=html.escape(topic.summary),
        part=html.escape(titleize(topic.part)),
        home="../../index.html",
        slide_buttons=slide_buttons,
        audio_block=audio_block,
        subtitles_link=subtitles_link,
        next_topic_button=next_topic_button,
        lesson_data=json_for_script(data),
        asset_version=asset_version(),
    )
    (out_dir / "index.html").write_text(html_text, encoding="utf-8")
    (out_dir / "transcript.txt").write_text(topic_transcript_text(topic), encoding="utf-8")
    (out_dir / "transcript.html").write_text(topic_transcript_html(topic), encoding="utf-8")


def topic_transcript_text(topic: Topic) -> str:
    lines = [topic.title, "=" * len(topic.title), ""]
    for slide in topic.slides:
        lines.append(f"Slide {slide.n}: {slide.title}")
        lines.append("")
        lines.append("Narration")
        lines.append(display_narration(slide.narration) or "[No narration text available.]")
        lines.append("")
        lines.append("On-screen text")
        lines.append(slide.text or "[No on-screen text available.]")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def topic_transcript_html(topic: Topic) -> str:
    sections = []
    for slide in topic.slides:
        sections.append(
            '<article class="transcript-slide">'
            f"<h2>Slide {slide.n}: {html.escape(slide.title)}</h2>"
            '<div class="transcript-grid">'
            '<section><h3>On-screen</h3>'
            f'<div class="static-slide">{slide.html}</div></section>'
            '<section><h3>Narration</h3>'
            f"<p>{html.escape(display_narration(slide.narration) or 'No narration text available.').replace(chr(10), '<br>')}</p></section>"
            "</div></article>"
        )
    return TRANSCRIPT_PAGE.format(
        title=html.escape(f"{topic.title} transcript"),
        heading=html.escape(topic.title),
        sections="\n".join(sections),
        asset_version=asset_version(),
    )


def render_index(parts: list[Part]) -> None:
    part_cards = []
    for part in parts:
        topic_cards = []
        for topic in part.topics:
            status = []
            status.append(f"{len(topic.slides)} slides")
            status.append("audio" if topic.audio else "audio pending")
            topic_cards.append(
                '<a class="topic-card" href="{href}">'
                '<strong>{title}</strong>'
                '<span>{summary}</span>'
                '<small>{status}</small>'
                "</a>".format(
                    href=html.escape(topic.output_path),
                    title=html.escape(topic.title),
                    summary=html.escape(topic.summary or "Self-paced topic page"),
                    status=html.escape(" / ".join(status)),
                )
            )
        part_cards.append(
            '<section class="part-band">'
            '<div class="part-copy">'
            f"<p>{html.escape(part.slug.upper())}</p>"
            f"<h2>{html.escape(part.title)}</h2>"
            f"<span>{html.escape(part.summary)}</span>"
            "</div>"
            f'<div class="topic-grid">{"".join(topic_cards)}</div>'
            "</section>"
        )
    index = INDEX_PAGE.format(parts="\n".join(part_cards), asset_version=asset_version())
    (ELEARNING / "index.html").write_text(index, encoding="utf-8")


def build_course_corpus(parts: list[Part]) -> None:
    topics = []
    slides = []
    for part in parts:
        for topic in part.topics:
            topics.append(
                {
                    "part": part.slug,
                    "topic": topic.slug,
                    "title": topic.title,
                    "summary": topic.summary,
                    "href": topic.output_path,
                    "slides": len(topic.slides),
                }
            )
            for slide in topic.slides:
                slides.append(
                    {
                        "part": part.slug,
                        "topic": topic.slug,
                        "topicTitle": topic.title,
                        "n": slide.n,
                        "title": slide.title,
                        "html": slide.html,
                        "text": slide.text,
                        "transcript": slide.narration,
                    }
                )
    corpus = {
        "course": "IT Professional Practice",
        "delivery": "elearning",
        "topics": topics,
        "slides": slides,
    }
    (ELEARNING / "course-corpus.json").write_text(json_for_script(corpus), encoding="utf-8")


def copy_textbook_assets(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for filename, _label in PUBLISHED_TEXTBOOK_FILES:
        source = TEXTBOOK / filename
        if source.exists():
            shutil.copy2(source, dest / filename)


def assemble_site() -> None:
    shutil.copytree(ELEARNING, SITE / "elearning")
    copy_textbook_assets(SITE / "textbook")
    (SITE / "index.html").write_text(SITE_INDEX.format(asset_version=asset_version()), encoding="utf-8")


def build() -> None:
    clean_output()
    write_assets()
    parts = load_course()
    topics = [topic for part in parts for topic in part.topics]
    for i, topic in enumerate(topics):
        next_topic = topics[i + 1] if i + 1 < len(topics) else None
        render_topic(topic, next_topic)
    render_index(parts)
    build_course_corpus(parts)
    copy_textbook_assets(ELEARNING / "textbook")
    assemble_site()
    topic_count = sum(len(part.topics) for part in parts)
    slide_count = sum(len(topic.slides) for part in parts for topic in part.topics)
    print(f"Built {topic_count} topics and {slide_count} slides under {ELEARNING.relative_to(ROOT)}")
    print(f"Assembled site under {SITE.relative_to(ROOT)}")


INDEX_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT Professional Practice</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="assets/course.css?v={asset_version}">
</head>
<body class="course-index">
<header class="site-hero">
  <nav>
    <a href="textbook/main.pdf">Textbook A4 PDF</a>
  </nav>
  <p>IT Professional Practice</p>
  <h1>Self-paced courseware for practical IT work</h1>
  <span>Browse modules, open interactive topic lessons, read transcripts, and use available audio without needing an LMS.</span>
</header>
<main>
{parts}
</main>
</body>
</html>
"""


SITE_INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT Professional Practice</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="elearning/assets/course.css?v={asset_version}">
</head>
<body class="course-index">
<header class="site-hero">
  <nav>
    <a href="elearning/">Interactive course</a>
    <a href="textbook/main.pdf">Textbook A4 PDF</a>
  </nav>
  <p>IT Professional Practice</p>
  <h1>Interactive courseware and printable textbook</h1>
  <span>Use the browser lessons for self-paced study, or download the LaTeX-generated textbook for student printing.</span>
</header>
<main>
  <section class="part-band">
    <div class="part-copy">
      <p>Course</p>
      <h2>Start learning</h2>
      <span>Open the interactive course surface with slide navigation, transcripts, and available media.</span>
    </div>
    <div class="topic-grid">
      <a class="topic-card" href="elearning/">
        <strong>Interactive lessons</strong>
        <span>Browse all topics as HTML e-learning pages.</span>
        <small>Open course</small>
      </a>
      <a class="topic-card" href="textbook/main.pdf">
        <strong>A4 textbook PDF</strong>
        <span>Student-printable LaTeX textbook generated from the same course source.</span>
        <small>Download PDF</small>
      </a>
    </div>
  </section>
</main>
</body>
</html>
"""


TOPIC_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="../../assets/course.css?v={asset_version}">
</head>
<body class="lesson-page">
<header class="lesson-topbar">
  <a href="{home}">IT Professional Practice</a>
  <span>{part}</span>
</header>
<main class="lesson-shell">
  <aside class="lesson-rail">
    <p>Topic</p>
    <h1>{title}</h1>
    <span>{summary}</span>
    <div class="lesson-meta">
      {audio_block}
      {subtitles_link}
      <a href="transcript.html">Transcript page</a>
      <a href="transcript.txt">Plain transcript</a>
    </div>
    <nav class="slide-list" aria-label="Slides">
      {slide_buttons}
    </nav>
  </aside>
  <section class="lesson-main">
    <div class="progress-track"><span id="progress-fill"></span></div>
    <div class="lesson-stage">
      <div class="slide-frame" id="slide-html" aria-live="polite"></div>
    </div>
    <div class="lesson-controls">
      <button id="prev-slide" type="button">Previous</button>
      <button id="subtitle-toggle" type="button" aria-pressed="false">Transcript overlay</button>
      <button id="next-slide" type="button">Next</button>
      {next_topic_button}
    </div>
    <div id="subtitle-box" hidden></div>
    <section id="local-qa" class="qa-card" hidden>
      <h2>Ask the course</h2>
      <p id="qa-status">Checking local model availability...</p>
      <form id="qa-form">
        <label for="qa-question">Question</label>
        <textarea id="qa-question" rows="3"></textarea>
        <button type="submit">Ask</button>
      </form>
      <pre id="qa-answer"></pre>
    </section>
  </section>
</main>
<script id="lesson-data" type="application/json">{lesson_data}</script>
<script src="../../assets/course.js?v={asset_version}"></script>
</body>
</html>
"""


TRANSCRIPT_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="../../assets/course.css?v={asset_version}">
</head>
<body class="transcript-page">
<main>
  <a href="index.html">Back to lesson</a>
  <h1>{heading}</h1>
  {sections}
</main>
</body>
</html>
"""


COURSE_CSS = """
:root {
  --ink: #18212f;
  --muted: #667085;
  --line: #d9e0ea;
  --surface: #ffffff;
  --soft: #f5f7f9;
  --green: #0f766e;
  --red: #b42318;
  --gold: #b7791f;
  --blue: #2f5f98;
  --slate: #243447;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(15, 118, 110, .16), transparent 34rem),
    linear-gradient(180deg, #eef2f5, #f8fafc 55%, #eef2f5);
  font-family: Charter, Georgia, "Times New Roman", serif;
}
a { color: var(--green); }
button, textarea {
  font: 700 14px/1.2 Avenir, "Trebuchet MS", sans-serif;
}
.site-hero {
  background:
    linear-gradient(90deg, rgba(24,33,47,.9), rgba(15,118,110,.7)),
    repeating-linear-gradient(135deg, #17202d 0 18px, #1d2a38 18px 36px);
  color: white;
  min-height: 44vh;
  padding: 34px max(28px, calc((100vw - 1180px) / 2)) 88px;
}
.site-hero nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-end;
  margin-bottom: 46px;
}
.site-hero nav a {
  color: white;
  border: 1px solid rgba(255,255,255,.32);
  border-radius: 999px;
  padding: 8px 13px;
  text-decoration: none;
  font: 700 13px/1 Avenir, "Trebuchet MS", sans-serif;
}
.site-hero p,
.lesson-rail > p {
  margin: 0 0 12px;
  font: 700 13px/1.2 Avenir, "Trebuchet MS", sans-serif;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.site-hero h1 {
  font-size: clamp(40px, 7vw, 84px);
  line-height: .98;
  max-width: 920px;
  margin: 0 0 24px;
}
.site-hero span {
  display: block;
  max-width: 760px;
  font: 22px/1.45 Avenir, "Trebuchet MS", sans-serif;
}
main {
  width: min(1180px, calc(100vw - 40px));
  margin: 0 auto;
}
.part-band {
  display: grid;
  grid-template-columns: minmax(220px, 310px) 1fr;
  gap: 28px;
  padding: 34px 0;
  border-bottom: 1px solid var(--line);
}
.part-copy h2 {
  margin: 0 0 10px;
  font-size: 30px;
}
.part-copy span,
.topic-card span,
.lesson-rail span {
  color: var(--muted);
  line-height: 1.45;
}
.topic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 12px;
}
.topic-card {
  display: grid;
  gap: 8px;
  min-height: 160px;
  padding: 18px;
  background: rgba(255,255,255,.9);
  border: 1px solid var(--line);
  border-radius: 8px;
  color: var(--ink);
  text-decoration: none;
  box-shadow: 0 12px 28px rgba(36, 52, 71, .08);
}
.topic-card strong { font-size: 18px; }
.topic-card small {
  align-self: end;
  color: var(--blue);
  font: 700 12px/1.2 Avenir, "Trebuchet MS", sans-serif;
  text-transform: uppercase;
}
.lesson-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px max(20px, calc((100vw - 1320px) / 2));
  color: white;
  background: var(--slate);
  font: 700 13px/1.2 Avenir, "Trebuchet MS", sans-serif;
}
.lesson-topbar a { color: white; text-decoration: none; }
.lesson-shell {
  width: min(1320px, calc(100vw - 28px));
  display: grid;
  grid-template-columns: 330px minmax(0, 1fr);
  gap: 20px;
  padding: 20px 0 42px;
}
.lesson-rail {
  position: sticky;
  top: 16px;
  align-self: start;
  max-height: calc(100vh - 32px);
  overflow: auto;
  padding: 22px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: 0 16px 36px rgba(36, 52, 71, .1);
}
.lesson-rail h1 {
  margin: 0 0 10px;
  font-size: 28px;
  line-height: 1.05;
}
.lesson-meta {
  display: grid;
  gap: 9px;
  margin: 20px 0;
  padding: 14px;
  background: var(--soft);
  border-radius: 12px;
  font: 700 13px/1.25 Avenir, "Trebuchet MS", sans-serif;
}
.lesson-meta audio {
  width: 100%;
}
.pending { color: var(--muted); }
.slide-list {
  display: grid;
  gap: 8px;
}
.slide-jump {
  display: grid;
  grid-template-columns: 42px 1fr;
  gap: 8px;
  width: 100%;
  text-align: left;
  padding: 11px 12px;
  color: var(--ink);
  background: white;
  border: 1px solid var(--line);
  border-radius: 10px;
  cursor: pointer;
}
.slide-jump.active {
  color: white;
  background: var(--green);
  border-color: var(--green);
}
.slide-jump span {
  color: inherit;
  font-family: Avenir, "Trebuchet MS", sans-serif;
}
.lesson-main {
  min-width: 0;
}
.progress-track {
  height: 9px;
  overflow: hidden;
  background: #d9e0ea;
  border-radius: 999px;
  margin-bottom: 16px;
}
#progress-fill {
  display: block;
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, var(--green), var(--gold));
  transition: width .25s ease;
}
.lesson-stage {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
}
.slide-frame,
.slide-copy,
.media-card,
.qa-card,
.transcript-slide {
  background: rgba(255,255,255,.96);
  border: 1px solid var(--line);
  border-radius: 16px;
  box-shadow: 0 18px 42px rgba(36, 52, 71, .1);
}
.slide-frame {
  min-height: clamp(560px, calc(100vh - 220px), 760px);
  display: grid;
  place-items: center;
  padding: clamp(18px, 3vw, 44px);
  overflow: auto;
}
.slide {
  width: min(100%, 1040px);
  min-height: 560px;
  display: grid;
  align-content: center;
  gap: 24px;
  padding: clamp(24px, 5vw, 70px);
  color: #101828;
  background:
    linear-gradient(145deg, rgba(255,255,255,.97), rgba(247,250,252,.98)),
    radial-gradient(circle at bottom right, rgba(15, 118, 110, .13), transparent 18rem);
  border: 1px solid #e5eaf0;
  border-radius: 18px;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.75);
}
.slide h1,
.slide h2 {
  margin: 0;
  font-size: clamp(34px, 5vw, 62px);
  line-height: .98;
}
.slide h3 {
  margin: 0;
  font-size: 28px;
}
.slide p,
.slide li,
.slide td,
.slide th {
  font-size: clamp(18px, 2vw, 25px);
  line-height: 1.35;
}
.slide ul,
.slide ol {
  margin: 0;
  padding-left: 1.25em;
}
.slide li + li { margin-top: .45em; }
.slide table {
  width: 100%;
  border-collapse: collapse;
  font-family: Avenir, "Trebuchet MS", sans-serif;
}
.slide th,
.slide td {
  border-bottom: 1px solid var(--line);
  padding: 10px;
  text-align: left;
  vertical-align: top;
}
.slide th {
  color: white;
  background: var(--slate);
}
.slide pre {
  white-space: pre-wrap;
  overflow: auto;
  padding: 18px;
  color: #e6edf3;
  background: #17202d;
  border-radius: 12px;
}
.slide code {
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: .82em;
}
.slide-figure {
  margin: 0;
  display: grid;
  place-items: center;
  gap: 12px;
}
.slide-figure img,
.slide img {
  max-width: 100%;
  max-height: 390px;
  object-fit: contain;
}
.slide-figure figcaption {
  color: var(--muted);
  font: 700 14px/1.2 Avenir, "Trebuchet MS", sans-serif;
}
/* In-slide diagrams: pure HTML/CSS replacements for generated raster art. */
.slide .diagram {
  width: 100%;
  font-family: Avenir, "Trebuchet MS", sans-serif;
  font-size: clamp(13px, 1.5vw, 16px);
  line-height: 1.3;
}
.slide .diagram-split {
  display: grid;
  grid-template-columns: minmax(0, .85fr) minmax(0, 1.15fr);
  gap: 24px;
  align-items: center;
}
.slide .diagram .dg-card {
  padding: .55em .8em;
  background: white;
  border: 2px solid var(--slate);
  border-radius: 10px;
}
.slide .diagram .dg-title {
  display: block;
  font-weight: 800;
}
.slide .diagram .dg-note {
  display: block;
  color: var(--muted);
  font-size: .88em;
}
.slide .diagram .dg-arrow {
  align-self: center;
  color: var(--slate);
  font-weight: 800;
  white-space: nowrap;
}
.slide .diagram .dg-caption {
  margin-top: .9em;
  color: var(--muted);
  font-weight: 700;
  font-size: .92em;
}
.slide .diagram .dg-badge {
  display: inline-block;
  margin-right: .6em;
  padding: .2em .7em;
  color: white;
  background: var(--slate);
  border-radius: 999px;
  font-weight: 800;
  font-size: .88em;
}
/* Decision guide: question rows routing to outcome cards. */
.slide .diagram-decision {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) auto minmax(0, 1fr);
  gap: .55em .7em;
  align-items: center;
}
.slide .diagram-decision .dg-question {
  padding: .5em .8em;
  background: var(--soft);
  border: 2px solid var(--blue);
  border-radius: 10px;
  font-weight: 700;
}
.slide .diagram-decision .dg-no {
  grid-column: 1;
  justify-self: center;
  color: var(--muted);
  font-weight: 700;
  font-size: .85em;
}
/* Escalation staircase with lanes. */
.slide .diagram-lanes {
  display: grid;
  grid-template-columns: 7.5em repeat(3, minmax(0, 1fr));
  gap: .5em .6em;
  align-items: center;
}
.slide .diagram-lanes .dg-lane {
  font-weight: 800;
  color: var(--slate);
  text-align: right;
  padding-right: .4em;
}
.slide .diagram-lanes .dg-arrow {
  text-align: right;
}
.slide .diagram-lanes .dg-return {
  grid-column: 2 / -1;
  padding: .45em .8em;
  background: var(--soft);
  border: 2px dashed var(--green);
  border-radius: 10px;
  font-weight: 700;
}
/* Metric shift rows: current state, arrow, target state. */
.slide .diagram-shift {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr) auto minmax(0, 1fr);
  gap: .5em .7em;
  align-items: center;
}
.slide .diagram-shift .dg-metric {
  font-weight: 800;
}
.slide .diagram-shift .dg-metric .dg-note {
  font-weight: 400;
}
.slide .diagram-shift .dg-current {
  padding: .4em .8em;
  text-align: center;
  background: #fdeaea;
  border: 2px solid #c0504d;
  border-radius: 999px;
  font-weight: 700;
}
.slide .diagram-shift .dg-target {
  padding: .4em .8em;
  text-align: center;
  background: #e7f4ef;
  border: 2px solid var(--green);
  border-radius: 999px;
  font-weight: 700;
}
/* Pipeline flow: stages joined by arrows, with an optional return path. */
.slide .diagram-flow {
  display: flex;
  align-items: stretch;
  gap: .45em;
}
.slide .diagram-flow .dg-card {
  flex: 1 1 0;
  min-width: 0;
}
.slide .diagram-flow + .dg-return-path,
.slide .diagram .dg-return-path {
  margin-top: .6em;
  padding: .45em .8em;
  text-align: right;
  color: #8a3b38;
  background: #fdf1f0;
  border: 2px dashed #c0504d;
  border-radius: 10px;
  font-weight: 700;
}
/* Milestone timeline: dots along a track with compact labels. */
.slide .diagram-timeline {
  position: relative;
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(0, 1fr);
  gap: .4em;
  text-align: center;
}
.slide .diagram-timeline::before {
  content: "";
  position: absolute;
  top: .4em;
  left: 4%;
  right: 4%;
  height: 4px;
  background: var(--line);
  border-radius: 999px;
}
.slide .diagram-timeline .dg-stop {
  display: grid;
  gap: .3em;
  justify-items: center;
}
.slide .diagram-timeline .dg-dot {
  position: relative;
  width: 1em;
  height: 1em;
  background: var(--green);
  border-radius: 50%;
  box-shadow: 0 0 0 3px #e7f4ef;
}
.slide .diagram-timeline .dg-stop:nth-child(even) .dg-dot {
  background: var(--blue);
  box-shadow: 0 0 0 3px var(--soft);
}
.slide-copy {
  padding: 22px;
}
#slide-counter {
  margin: 0 0 8px;
  color: var(--blue);
  font: 700 13px/1 Avenir, "Trebuchet MS", sans-serif;
  letter-spacing: .06em;
  text-transform: uppercase;
}
.slide-copy h2 {
  margin: 0 0 18px;
  font-size: 30px;
  line-height: 1.1;
}
details {
  margin-top: 13px;
  padding-top: 13px;
  border-top: 1px solid var(--line);
}
summary {
  cursor: pointer;
  font: 700 14px/1.2 Avenir, "Trebuchet MS", sans-serif;
}
.lesson-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: space-between;
  margin: 16px 0;
}
.lesson-controls button,
.lesson-controls .next-topic-button,
.qa-card button {
  border: 0;
  border-radius: 999px;
  padding: 12px 16px;
  color: white;
  background: var(--slate);
  cursor: pointer;
}
.lesson-controls .next-topic-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-left: auto;
  background: var(--green);
  text-decoration: none;
}
.lesson-controls .next-topic-button[hidden] {
  display: none;
}
.lesson-controls button:disabled {
  cursor: not-allowed;
  opacity: .45;
}
.lesson-controls button[aria-pressed="true"] {
  background: var(--green);
}
#subtitle-box {
  position: sticky;
  bottom: 18px;
  z-index: 2;
  margin: 0 auto 14px;
  width: min(900px, 92%);
  padding: 14px 18px;
  color: white;
  background: rgba(24, 33, 47, .92);
  border-radius: 14px;
  box-shadow: 0 18px 40px rgba(24,33,47,.28);
  font: 18px/1.45 Avenir, "Trebuchet MS", sans-serif;
}
.media-card,
.qa-card {
  margin-top: 18px;
  padding: 20px;
}
.qa-card textarea {
  width: 100%;
  margin: 8px 0 10px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 10px;
}
.qa-card pre {
  white-space: pre-wrap;
  font-family: Avenir, "Trebuchet MS", sans-serif;
}
.transcript-page main {
  max-width: 1120px;
  padding: 32px 0 60px;
}
.transcript-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(300px, .7fr);
  gap: 18px;
}
.transcript-slide {
  margin: 18px 0;
  padding: 20px;
}
.static-slide .slide {
  min-height: 320px;
  transform-origin: top left;
}
.site-forward main {
  padding: 48px 0;
}
@media (max-width: 980px) {
  .part-band,
  .lesson-shell,
  .lesson-stage,
  .transcript-grid {
    grid-template-columns: 1fr;
  }
  .lesson-rail {
    position: static;
    max-height: none;
  }
  .slide-frame {
    min-height: 420px;
    padding: 12px;
  }
  .slide {
    min-height: 380px;
  }
}
"""


COURSE_JS = """
(() => {
  const dataEl = document.getElementById('lesson-data');
  if (!dataEl) return;
  const lesson = JSON.parse(dataEl.textContent);
  const slides = lesson.slides || [];
  const storageKey = `professional-practice:${lesson.topicPath}:slide`;
  const frame = document.getElementById('slide-html');
  const counter = document.getElementById('slide-counter');
  const title = document.getElementById('slide-title');
  const narration = document.getElementById('slide-narration');
  const onscreen = document.getElementById('slide-onscreen');
  const progress = document.getElementById('progress-fill');
  const prev = document.getElementById('prev-slide');
  const next = document.getElementById('next-slide');
  const nextTopic = document.getElementById('next-topic');
  const subtitleToggle = document.getElementById('subtitle-toggle');
  const subtitleBox = document.getElementById('subtitle-box');
  const audio = document.getElementById('audio-player');
  const jumps = Array.from(document.querySelectorAll('.slide-jump'));
  const slideTimings = (lesson.slideTimings || [])
    .filter((timing) => Number.isFinite(timing.index) && Number.isFinite(timing.start))
    .sort((a, b) => a.index - b.index);
  let index = Math.min(Math.max(Number(localStorage.getItem(storageKey)) || 0, 0), Math.max(slides.length - 1, 0));
  let primedAudioForStoredSlide = false;
  let pendingAudioSeek = null;
  let suppressAudioSyncUntil = 0;

  function timingForSlide(slideIndex) {
    return slideTimings.find((timing) => timing.index === slideIndex) || null;
  }

  function slideIndexForTime(seconds) {
    if (!slideTimings.length) return index;
    let matched = slideTimings[0].index || 0;
    for (const timing of slideTimings) {
      if (seconds + 0.05 >= timing.start) matched = timing.index;
      if (Number.isFinite(timing.end) && seconds < timing.end - 0.05) break;
    }
    return Math.min(Math.max(matched, 0), Math.max(slides.length - 1, 0));
  }

  function seekAudioToSlide(slideIndex) {
    if (!audio) return;
    const timing = timingForSlide(slideIndex);
    if (!timing) return;
    const targetTime = Math.max(0, timing.start + 0.01);
    pendingAudioSeek = targetTime;
    suppressAudioSyncUntil = Date.now() + 1000;
    if (audio.readyState === 0) {
      audio.load();
    }
    try {
      audio.currentTime = targetTime;
      pendingAudioSeek = null;
    } catch (error) {
      // Some browsers reject seeks before metadata is available.
    }
  }

  function render(options = {}) {
    const slide = slides[index];
    if (!slide) return;
    if (frame) frame.innerHTML = slide.html || '<section class="slide"><p>Slide content pending.</p></section>';
    if (counter) counter.textContent = `Slide ${index + 1} of ${slides.length}`;
    if (title) title.textContent = slide.title || `Slide ${index + 1}`;
    if (narration) narration.textContent = slide.narration || 'No narration text available.';
    if (onscreen) onscreen.textContent = slide.text || 'No on-screen text available.';
    if (progress) progress.style.width = `${((index + 1) / slides.length) * 100}%`;
    if (prev) prev.disabled = index === 0;
    if (next) next.disabled = index === slides.length - 1;
    if (nextTopic) nextTopic.hidden = index !== slides.length - 1;
    jumps.forEach((button, i) => button.classList.toggle('active', i === index));
    if (subtitleBox && !subtitleBox.hidden) subtitleBox.textContent = slide.narration || slide.title || '';
    localStorage.setItem(storageKey, String(index));
    if (options.seekAudio) seekAudioToSlide(index);
  }

  function goToSlide(slideIndex, options = {}) {
    const nextIndex = Math.min(Math.max(slideIndex, 0), Math.max(slides.length - 1, 0));
    index = nextIndex;
    render(options);
  }

  prev?.addEventListener('click', () => {
    goToSlide(index - 1, { seekAudio: true });
  });
  next?.addEventListener('click', () => {
    goToSlide(index + 1, { seekAudio: true });
  });
  jumps.forEach((button) => {
    button.addEventListener('click', () => {
      goToSlide(Number(button.dataset.slide || 0), { seekAudio: true });
    });
  });
  document.addEventListener('keydown', (event) => {
    if (event.target && ['TEXTAREA', 'INPUT'].includes(event.target.tagName)) return;
    if (event.key === 'ArrowLeft') prev?.click();
    if (event.key === 'ArrowRight') next?.click();
  });
  subtitleToggle?.addEventListener('click', () => {
    if (!subtitleBox) return;
    const enabled = subtitleToggle.getAttribute('aria-pressed') !== 'true';
    subtitleToggle.setAttribute('aria-pressed', String(enabled));
    subtitleBox.hidden = !enabled;
    render();
  });
  audio?.addEventListener('play', () => {
    if (!primedAudioForStoredSlide && audio.currentTime < 0.25 && index > 0) {
      seekAudioToSlide(index);
    }
    primedAudioForStoredSlide = true;
  });
  audio?.addEventListener('loadedmetadata', () => {
    if (pendingAudioSeek === null) return;
    suppressAudioSyncUntil = Date.now() + 1000;
    try {
      audio.currentTime = pendingAudioSeek;
      pendingAudioSeek = null;
    } catch (error) {
      // Leave the pending seek in place; the next metadata/load event can retry.
    }
  });
  audio?.addEventListener('seeked', () => {
    suppressAudioSyncUntil = 0;
  });
  audio?.addEventListener('timeupdate', () => {
    if (Date.now() < suppressAudioSyncUntil) return;
    const syncedIndex = slideIndexForTime(audio.currentTime);
    if (syncedIndex !== index) {
      goToSlide(syncedIndex);
    } else if (subtitleBox && !subtitleBox.hidden) {
      const slide = slides[index];
      subtitleBox.textContent = slide?.narration || slide?.title || '';
    }
  });
  audio?.addEventListener('ended', () => {
    goToSlide(slides.length - 1);
  });

  async function maybeEnableLocalQa() {
    const card = document.getElementById('local-qa');
    const status = document.getElementById('qa-status');
    const form = document.getElementById('qa-form');
    const question = document.getElementById('qa-question');
    const answer = document.getElementById('qa-answer');
    if (!card || !status || !form || !question || !answer) return;
    const api = window.LanguageModel || window.ai?.languageModel;
    if (!api?.availability || !api?.create) return;
    let availability = 'unavailable';
    try {
      availability = await api.availability();
    } catch (error) {
      return;
    }
    if (availability !== 'available') {
      return;
    }
    card.hidden = false;
    status.textContent = 'Local model is available. Answers stay in this browser.';
    const corpus = await fetch('../../course-corpus.json').then((response) => response.json()).catch(() => null);
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const q = question.value.trim();
      if (!q) return;
      answer.textContent = 'Thinking...';
      const context = JSON.stringify(corpus || lesson).slice(0, 22000);
      try {
        const session = await api.create();
        const result = await session.prompt(`Answer using only this IT Professional Practice course context. If the answer is not in the context, say so.\\n\\nContext:\\n${context}\\n\\nQuestion: ${q}`);
        answer.textContent = result;
      } catch (error) {
        answer.textContent = `Local model request failed: ${error}`;
      }
    });
  }

  render();
  maybeEnableLocalQa();
})();
"""


if __name__ == "__main__":
    build()
