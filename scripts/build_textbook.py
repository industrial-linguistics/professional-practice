#!/usr/bin/env python3
"""Build the LaTeX textbook project from course HTML slides and narratives."""

from __future__ import annotations

import html
import re
import shutil
import subprocess
from pathlib import Path

from course_content import ROOT, Part, Slide, Topic, load_course, narrative_files


TEXTBOOK = ROOT / "textbook"
CHAPTERS = TEXTBOOK / "chapters"
FIGURES = TEXTBOOK / "figures"
AUDIT = TEXTBOOK / "audit"


def slug(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def tex_escape(value: str) -> str:
    value = (
        value.replace("\u00a0", " ")
        .replace("\u202f", " ")
        .replace("\u2009", " ")
        .replace("\u2011", "-")
        .replace("\ufe0f", "")
    )
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "≠": r"$\ne$",
        "≤": r"$\le$",
        "≥": r"$\ge$",
        "✅": r"[OK]",
        "⚠": r"[Warning]",
        "❌": r"[Fail]",
        "➜": r"$\rightarrow$",
        "↔": r"$\leftrightarrow$",
        "│": "|",
        "├": "|",
        "└": "`",
        "─": "-",
    }
    return "".join(replacements.get(ch, ch) for ch in value)


def normalise_code(value: str) -> str:
    replacements = {
        "\u2502": "|",
        "\u251c": "|",
        "\u2514": "`",
        "\u2500": "-",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2194": "<->",
        "\u2193": "v",
        "\u2191": "^",
        "\u279c": "->",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2260": "!=",
    }
    return "".join(replacements.get(ch, ch) for ch in value)


def tex_heading(value: str) -> str:
    return tex_escape(re.sub(r"\s+", " ", value).strip())


def clean_generated() -> None:
    TEXTBOOK.mkdir(exist_ok=True)
    for path in [CHAPTERS, FIGURES, AUDIT]:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
    for stale in [TEXTBOOK / "index.html"]:
        if stale.exists():
            stale.unlink()


def copy_topic_images(topic: Topic) -> None:
    src = topic.source_path / "images"
    if not src.exists():
        return
    dest = FIGURES / topic.part / topic.slug / "images"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)


def image_alt(slide: Slide, src: str) -> str:
    pattern = re.compile(
        rf"<img\b[^>]*src=[\"']{re.escape(src)}[\"'][^>]*>",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(slide.html)
    if not match:
        return slide.title
    alt_match = re.search(r"\balt=([\"'])(.*?)\1", match.group(0), re.DOTALL)
    if not alt_match:
        return slide.title
    return html.unescape(alt_match.group(2)).strip() or slide.title


def paragraph_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines()]


def tex_text_block(text: str) -> str:
    lines = paragraph_lines(text)
    out: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append(tex_escape(" ".join(paragraph)))
            out.append("")
            paragraph.clear()

    def flush_bullets() -> None:
        if bullets:
            out.append(r"\begin{itemize}[leftmargin=*]")
            out.extend(rf"\item {tex_escape(item)}" for item in bullets)
            out.append(r"\end{itemize}")
            out.append("")
            bullets.clear()

    for line in lines:
        if not line:
            flush_paragraph()
            flush_bullets()
            continue
        if line.startswith("- "):
            flush_paragraph()
            bullets.append(line[2:].strip())
        else:
            flush_bullets()
            paragraph.append(line)
    flush_paragraph()
    flush_bullets()
    return "\n".join(out).strip()


def is_title_slide(slide: Slide) -> bool:
    start = slide.html.split(">", 1)[0].lower()
    return 'data-kind="title"' in start or "data-kind='title'" in start or slide.n == 1


def narrative_to_book_prose(text: str) -> str:
    text = re.sub(r"(?im)^\s*Speaker\s+\d+:\s*", "", text)
    text = re.sub(r"\[[^\]]+\]\s*", "", text)
    text = re.sub(r"\bWelcome to\b", "This section begins with", text, flags=re.IGNORECASE)
    text = re.sub(r"\btoday\b", "this section", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""

    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs: list[str] = []
    current: list[str] = []
    for sentence in sentences:
        if not sentence:
            continue
        current.append(sentence)
        if len(" ".join(current)) >= 360:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)


def slide_key_points(slide: Slide) -> list[str]:
    points: list[str] = []
    seen: set[str] = set()
    title = re.sub(r"\s+", " ", slide.title).strip().lower()
    for raw in slide.text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip(" -\t")
        if not line:
            continue
        if line.lower() == title:
            continue
        if line.startswith("Image:"):
            continue
        if len(line) > 170:
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        points.append(line)
    return points[:6]


def tex_itemize(items: list[str]) -> str:
    if not items:
        return ""
    lines = [r"\begin{itemize}[leftmargin=*]"]
    lines.extend(rf"\item {tex_escape(item)}" for item in items)
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def pre_blocks(slide: Slide) -> list[str]:
    blocks = []
    for match in re.finditer(
        r"<pre><code(?:\s+[^>]*)?>(.*?)</code></pre>",
        slide.html,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        blocks.append(html.unescape(match.group(1)).strip("\n"))
    return blocks


def render_slide(topic: Topic, slide: Slide, *, include_heading: bool = True) -> str:
    parts: list[str] = []
    if include_heading:
        parts.append(rf"\subsection{{{tex_heading(slide.title)}}}")
        parts.append(rf"\index{{{tex_escape(slide.title)}}}")

    if slide.narration:
        prose = narrative_to_book_prose(slide.narration)
        if prose:
            parts.append(tex_text_block(prose))
    else:
        points = slide_key_points(slide)
        if points:
            parts.append(tex_text_block("This section should be expanded from the following practice points."))
            parts.append(tex_itemize(points))

    for src in slide.image_paths:
        if re.match(r"^[a-z]+:", src) or src.startswith("/"):
            continue
        source = topic.source_path / src
        if not source.exists():
            continue
        rel = Path("figures") / topic.part / topic.slug / src
        caption = image_alt(slide, src)
        parts.append(
            "\n".join(
                [
                    r"\begin{figure}[htbp]",
                    r"\centering",
                    rf"\includegraphics[width=0.86\linewidth]{{{rel.as_posix()}}}",
                    rf"\caption{{{tex_escape(caption)}}}",
                    r"\end{figure}",
                ]
            )
        )

    code_blocks = pre_blocks(slide)
    if code_blocks:
        parts.append(r"\paragraph{Example artifact.}")
        for code in code_blocks:
            parts.append(r"\begin{CodeBlock}")
            parts.append(normalise_code(code))
            parts.append(r"\end{CodeBlock}")
    else:
        points = slide_key_points(slide)
        if points and not is_title_slide(slide):
            parts.append(r"\paragraph{Practice checkpoints.}")
            parts.append(tex_itemize(points))

    return "\n\n".join(part for part in parts if part.strip())


def render_topic(topic: Topic) -> str:
    copy_topic_images(topic)
    lines = [
        rf"\section{{{tex_heading(topic.title)}}}",
        rf"\index{{{tex_escape(topic.title)}}}",
    ]
    slides = topic.slides
    if slides and is_title_slide(slides[0]):
        opener = render_slide(topic, slides[0], include_heading=False)
        if opener:
            lines.extend([opener, ""])
        slides = slides[1:]
    elif topic.summary:
        lines.extend([tex_text_block(topic.summary), ""])

    for slide in slides:
        lines.append(render_slide(topic, slide))
        lines.append("")
    return "\n".join(lines)


def render_part(part: Part) -> str:
    body = [
        "% Generated by scripts/build_textbook.py; edit content/ and rebuild.",
        rf"\chapter{{{tex_heading(part.title)}}}",
        rf"\index{{{tex_escape(part.title)}}}",
    ]
    if part.summary:
        body.append(tex_text_block(part.summary))
    for topic in part.topics:
        body.append(render_topic(topic))
    return "\n\n".join(body).strip() + "\n"


def write_main(parts: list[Part]) -> None:
    includes = "\n".join(
        rf"\include{{chapters/{part.slug}-{slug(part.title)}}}" for part in parts
    )
    (TEXTBOOK / "main.tex").write_text(MAIN_TEX.replace("@@INCLUDES@@", includes), encoding="utf-8")
    (TEXTBOOK / "main-amazon.tex").write_text(
        "\\def\\amazontrimsize{}\n\\def\\omitcoverpage{}\n\\input{main.tex}\n",
        encoding="utf-8",
    )
    (TEXTBOOK / "Makefile").write_text(MAKEFILE, encoding="utf-8")
    (TEXTBOOK / "README.md").write_text(README, encoding="utf-8")


def write_chapters(parts: list[Part]) -> None:
    for part in parts:
        path = CHAPTERS / f"{part.slug}-{slug(part.title)}.tex"
        path.write_text(render_part(part), encoding="utf-8")


def write_audit(parts: list[Part]) -> None:
    topics = sum(len(part.topics) for part in parts)
    slides = sum(len(topic.slides) for part in parts for topic in part.topics)
    mismatches = []
    for part in parts:
        for topic in part.topics:
            narratives = narrative_files(topic.source_path)
            if len(narratives) != len(topic.slides):
                mismatches.append((topic, len(narratives)))
    (AUDIT / "open-issues.md").write_text(
        "# Textbook Open Issues\n\n"
        f"- Generated from {len(parts)} parts, {topics} topics and {slides} slides.\n"
        f"- {len(mismatches)} topics currently have slide/narrative count mismatches; "
        "see `docs/narrative-mismatch-audit.md`.\n"
        "- The generator now renders narrative material as textbook prose and keeps slide text as practice checkpoints; later editorial passes should still improve examples and continuity by hand.\n",
        encoding="utf-8",
    )
    (AUDIT / "style-notes.md").write_text(
        "# Style Notes\n\n"
        "- Preserve the practical, professional-practice teaching voice from the existing narratives.\n"
        "- Later passes should convert slide-fragment pacing into smoother chapter prose where useful.\n",
        encoding="utf-8",
    )
    (AUDIT / "slop-patterns.md").write_text(
        "# Slop Patterns\n\n"
        "- Avoid generic motivational bridge prose when expanding the slide-derived chapters.\n",
        encoding="utf-8",
    )


def build_pdf() -> None:
    subprocess.run(["make", "-C", str(TEXTBOOK)], check=True)


def build() -> None:
    clean_generated()
    parts = load_course()
    write_chapters(parts)
    write_main(parts)
    write_audit(parts)
    build_pdf()
    topics = sum(len(part.topics) for part in parts)
    slides = sum(len(topic.slides) for part in parts for topic in part.topics)
    print(f"Built LaTeX textbook with {topics} topics and {slides} slides")


MAIN_TEX = r"""\documentclass[11pt,openany]{book}
\ifdefined\amazontrimsize
  \usepackage[paperwidth=6in,paperheight=9in,margin=0.72in]{geometry}
\else
  \usepackage[a4paper,margin=2.6cm]{geometry}
\fi
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{makeidx}
\usepackage{setspace}
\usepackage[nopatch=footnote]{microtype}
\usepackage{fvextra}
\usepackage{xcolor}
\usepackage{float}
\DefineVerbatimEnvironment{CodeBlock}{Verbatim}{breaklines=true,breakanywhere=true,fontsize=\small}
\makeindex
\setstretch{1.14}
\setcounter{tocdepth}{1}
\setlength{\emergencystretch}{3em}
\sloppy
\pagestyle{plain}
\hypersetup{
  pdftitle={IT Professional Practice},
  pdfauthor={Greg Baker},
  hidelinks
}
\title{IT Professional Practice\\\large A Practical Course Reader}
\author{Greg Baker}
\date{Draft edition}
\newif\ifcoverpage
\coverpagetrue
\ifdefined\omitcoverpage
  \coverpagefalse
\fi

\begin{document}
\ifcoverpage
\begin{titlepage}
\thispagestyle{empty}
\vspace*{0.12\textheight}
{\Huge\bfseries IT Professional Practice\par}
\vspace{1.2em}
{\Large A Practical Course Reader\par}
\vfill
{\large Greg Baker\par}
{\large Draft edition\par}
\end{titlepage}
\fi

\frontmatter
\tableofcontents
\mainmatter
@@INCLUDES@@
\backmatter
\cleardoublepage
\phantomsection
\addcontentsline{toc}{chapter}{Index}
{\footnotesize\raggedright\printindex}
\end{document}
"""


MAKEFILE = r"""TEX=main.tex
AMAZON_TEX=main-amazon.tex
PDF=main.pdf
AMAZON_PDF=main-amazon.pdf
LATEXMK=latexmk -xelatex -quiet -e '$$max_repeat=10'
BASE=$(basename $(TEX))
AMAZON_BASE=$(basename $(AMAZON_TEX))
CHAPTERS=$(wildcard chapters/*.tex)
FIGURES=$(shell find figures -type f 2>/dev/null)

all: $(PDF) $(AMAZON_PDF)

$(PDF): $(TEX) $(CHAPTERS) $(FIGURES)
	$(LATEXMK) $(TEX)
	makeindex $(BASE) >/dev/null || true
	$(LATEXMK) $(TEX)

$(AMAZON_PDF): $(AMAZON_TEX) $(TEX) $(CHAPTERS) $(FIGURES)
	$(LATEXMK) $(AMAZON_TEX)
	makeindex $(AMAZON_BASE) >/dev/null || true
	$(LATEXMK) $(AMAZON_TEX)

free-pdf: $(PDF)

amazon-pdf: $(AMAZON_PDF)

clean:
	latexmk -C $(TEX) || true
	latexmk -C $(AMAZON_TEX) || true
	rm -f $(BASE).idx $(BASE).ind $(BASE).ilg $(AMAZON_BASE).idx $(AMAZON_BASE).ind $(AMAZON_BASE).ilg

.PHONY: all free-pdf amazon-pdf clean
"""


README = """# IT Professional Practice Textbook

This directory contains the generated LaTeX textbook project for the course.
It is generated from `content/part-*/topic/slides.html` and `narratives/` by
`scripts/build_textbook.py`.

Build both student-print and Amazon print-on-demand PDFs with:

```bash
make -C textbook
```

Outputs:

- `textbook/main.pdf`: A4 PDF for student printing.
- `textbook/main-amazon.pdf`: 6x9 inch PDF for Amazon KDP-style print-on-demand.

Do not edit generated chapter files directly; edit course source and rebuild.
"""


if __name__ == "__main__":
    build()
