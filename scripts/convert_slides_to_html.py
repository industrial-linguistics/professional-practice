#!/usr/bin/env python3
"""Convert legacy ``slides.md`` files to editable HTML slide source."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


def parse_front_matter(markdown: str) -> tuple[dict[str, str], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---", 4)
    if end == -1:
        return {}, markdown
    raw = markdown[4:end]
    body = markdown[end + 4 :].lstrip()
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, body


def split_slides(body: str) -> list[str]:
    chunks = re.split(r"\n---[ \t]*\n", body.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def inline_markdown(text: str) -> str:
    placeholders: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\u0000{len(placeholders) - 1}\u0000"

    text = re.sub(r"`([^`]+)`", stash_code, text)
    escaped = html.escape(text, quote=False)

    def image(match: re.Match[str]) -> str:
        alt = html.escape(html.unescape(match.group(1)), quote=True)
        src = html.escape(html.unescape(match.group(2)), quote=True)
        return f'<img src="{src}" alt="{alt}">'

    def link(match: re.Match[str]) -> str:
        label = inline_markdown(html.unescape(match.group(1)))
        href = html.escape(html.unescape(match.group(2)), quote=True)
        return f'<a href="{href}">{label}</a>'

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image, escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"_([^_]+)_", r"<em>\1</em>", escaped)
    for i, value in enumerate(placeholders):
        escaped = escaped.replace(f"\u0000{i}\u0000", value)
    return escaped


def plain_text(markdown: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", markdown)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^[#>*\-\s]+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def heading_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^\s*#{1,4}\s+(.+?)\s*$", line)
        if match:
            return plain_text(match.group(1)) or fallback
    text = plain_text(markdown)
    return text[:80].strip() or fallback


def table_to_html(lines: list[str]) -> str:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) >= 2 and all(re.fullmatch(r":?-{3,}:?", cell or "---") for cell in rows[1]):
        header = rows[0]
        body = rows[2:]
    else:
        header = []
        body = rows
    out = ["<table>"]
    if header:
        out.append("<thead><tr>")
        out.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
        out.append("</tr></thead>")
    out.append("<tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


class BlockWriter:
    def __init__(self) -> None:
        self.out: list[str] = []
        self.paragraph: list[str] = []
        self.lists: list[dict[str, object]] = []

    def flush_paragraph(self) -> None:
        if self.paragraph:
            self.out.append(f"<p>{inline_markdown(' '.join(self.paragraph))}</p>")
            self.paragraph = []

    def close_lists_to(self, depth: int = 0) -> None:
        self.flush_paragraph()
        while len(self.lists) > depth:
            state = self.lists[-1]
            if state.get("li_open"):
                self.out.append("</li>")
            self.out.append(f"</{state['tag']}>")
            self.lists.pop()

    def open_list(self, tag: str) -> None:
        self.out.append(f"<{tag}>")
        self.lists.append({"tag": tag, "indent": 0, "li_open": False})

    def add_list_item(self, indent: int, tag: str, text: str) -> None:
        self.flush_paragraph()
        while self.lists and int(self.lists[-1]["indent"]) > indent:
            self.close_lists_to(len(self.lists) - 1)
        if self.lists and int(self.lists[-1]["indent"]) == indent and self.lists[-1]["tag"] != tag:
            self.close_lists_to(len(self.lists) - 1)
        if not self.lists or int(self.lists[-1]["indent"]) < indent:
            self.out.append(f"<{tag}>")
            self.lists.append({"tag": tag, "indent": indent, "li_open": False})
        state = self.lists[-1]
        if state.get("li_open"):
            self.out.append("</li>")
        self.out.append(f"<li>{inline_markdown(text)}")
        state["li_open"] = True

    def finish(self) -> str:
        self.close_lists_to(0)
        self.flush_paragraph()
        return "\n".join(self.out)


def slide_markdown_to_html(markdown: str) -> str:
    writer = BlockWriter()
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        if not stripped:
            writer.flush_paragraph()
            i += 1
            continue
        if stripped.startswith("```"):
            writer.close_lists_to(0)
            fence_lang = stripped[3:].strip()
            code: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i].rstrip("\n"))
                i += 1
            i += 1
            lang_attr = f' class="language-{html.escape(fence_lang, quote=True)}"' if fence_lang else ""
            writer.out.append(f"<pre><code{lang_attr}>{html.escape(chr(10).join(code))}</code></pre>")
            continue
        if re.match(r"^\|.*\|$", stripped):
            table_lines = [stripped]
            i += 1
            while i < len(lines) and re.match(r"^\|.*\|$", lines[i].strip()):
                table_lines.append(lines[i].strip())
                i += 1
            writer.close_lists_to(0)
            writer.out.append(table_to_html(table_lines))
            continue
        heading = re.match(r"^(#{1,4})\s+(.+?)\s*$", stripped)
        if heading:
            writer.close_lists_to(0)
            level = min(len(heading.group(1)), 4)
            writer.out.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            i += 1
            continue
        image_only = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped)
        if image_only:
            writer.close_lists_to(0)
            alt = html.escape(image_only.group(1), quote=False)
            src = html.escape(image_only.group(2), quote=True)
            caption = f"<figcaption>{alt}</figcaption>" if alt else ""
            writer.out.append(f'<figure class="slide-figure"><img src="{src}" alt="{alt}">{caption}</figure>')
            i += 1
            continue
        list_item = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", line)
        if list_item:
            indent = len(list_item.group(1).replace("\t", "    "))
            marker = list_item.group(2)
            tag = "ol" if marker.endswith(".") else "ul"
            writer.add_list_item(indent, tag, list_item.group(3).strip())
            i += 1
            continue
        writer.close_lists_to(0)
        writer.paragraph.append(stripped)
        i += 1
    return writer.finish()


def convert_file(path: Path, *, delete_markdown: bool = False, force: bool = False) -> Path:
    front, body = parse_front_matter(path.read_text(encoding="utf-8"))
    slides = split_slides(body)
    out_path = path.with_name("slides.html")
    if out_path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite {out_path}; pass --force")
    parts = [
        "<!-- Generated from legacy slide Markdown by scripts/convert_slides_to_html.py. -->",
        f"<!-- title: {html.escape(front.get('title', path.parent.name), quote=False)} -->",
        "",
    ]
    for i, slide_md in enumerate(slides, start=1):
        title = heading_title(slide_md, f"Slide {i}")
        kind = "title" if i == 1 else "content"
        parts.append(
            f'<section class="slide" data-slide="{i}" data-kind="{kind}" '
            f'data-title="{html.escape(title, quote=True)}">'
        )
        parts.append(slide_markdown_to_html(slide_md))
        parts.append("</section>")
        parts.append("")
    out_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    if delete_markdown:
        path.unlink()
    return out_path


def slides_md_files(content_dir: Path) -> list[Path]:
    return sorted(content_dir.glob("part-*/*/slides.md"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, help="Specific slides.md files or topic dirs")
    parser.add_argument("--content-dir", type=Path, default=CONTENT)
    parser.add_argument("--delete-markdown", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    paths: list[Path] = []
    if args.paths:
        for path in args.paths:
            paths.append(path / "slides.md" if path.is_dir() else path)
    else:
        paths = slides_md_files(args.content_dir)
    if not paths:
        raise SystemExit("No slides.md files found")
    for path in paths:
        converted = convert_file(path, delete_markdown=args.delete_markdown, force=args.force)
        print(converted)


if __name__ == "__main__":
    main()
