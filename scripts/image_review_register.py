#!/usr/bin/env python3
"""Register a generated image candidate for the protected review site."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sqlite3
from pathlib import Path


DEFAULT_DB = Path("state/image-review/image-review.sqlite")
PUBLIC_PREFIX = "/image-review/candidates"


SCHEMA = """
CREATE TABLE IF NOT EXISTS candidates (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL DEFAULT '',
    target_path TEXT NOT NULL,
    topic_path TEXT NOT NULL DEFAULT '',
    slide_ref TEXT NOT NULL DEFAULT '',
    brief TEXT NOT NULL DEFAULT '',
    prompt TEXT NOT NULL DEFAULT '',
    candidate_url TEXT NOT NULL,
    current_slide_url TEXT NOT NULL,
    proposed_slide_url TEXT NOT NULL,
    candidate_rel_path TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'approved', 'rejected', 'commented', 'processed')),
    review_comment TEXT NOT NULL DEFAULT '',
    reviewed_by TEXT,
    reviewed_at TEXT,
    processed_at TEXT,
    requeued_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT NOT NULL,
    actor TEXT NOT NULL DEFAULT '',
    action TEXT NOT NULL,
    comment TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status, created_at);
CREATE INDEX IF NOT EXISTS idx_review_events_candidate ON review_events(candidate_id, created_at);
"""


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value[:72] or "candidate"


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8").strip()
    return (args.prompt or "").strip()


def default_id(batch_id: str, target_path: str) -> str:
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d%H%M%S")
    return f"{slug(batch_id)}-{slug(target_path)}-{stamp}"


def ensure_batch_file(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    path.write_text(
        f"# Image review batch {today}\n\n"
        "| Candidate | Target | Slide | Brief | Review URL |\n"
        "| --- | --- | --- | --- | --- |\n",
        encoding="utf-8",
    )


def append_batch_row(path: Path, row: dict[str, str], review_base_url: str) -> None:
    ensure_batch_file(path)
    review_url = f"{review_base_url}#{slug(row['id'])}"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"| `{row['id']}` | `{row['target_path']}` | {row['slide_ref'] or '-'} "
            f"| {row['brief']} | {review_url} |\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--id")
    parser.add_argument("--batch-id", default=dt.date.today().isoformat())
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--topic-path", default="")
    parser.add_argument("--slide-ref", default="")
    parser.add_argument("--brief", required=True)
    parser.add_argument("--prompt", default="")
    parser.add_argument("--prompt-file")
    parser.add_argument("--candidate-url")
    parser.add_argument("--current-slide-url")
    parser.add_argument("--proposed-slide-url")
    parser.add_argument("--candidate-rel-path")
    parser.add_argument("--batch-file", type=Path)
    parser.add_argument(
        "--review-base-url",
        default="https://professional-practice.industrial-linguistics.com/cgi-bin/image-review.cgi",
    )
    args = parser.parse_args()

    candidate_id = args.id or default_id(args.batch_id, args.target_path)
    candidate_rel_path = args.candidate_rel_path or f"{candidate_id}/candidate.png"
    candidate_url = args.candidate_url or f"{PUBLIC_PREFIX}/{candidate_rel_path}"
    current_slide_url = args.current_slide_url or f"{PUBLIC_PREFIX}/{candidate_id}/current-slide.png"
    proposed_slide_url = args.proposed_slide_url or f"{PUBLIC_PREFIX}/{candidate_id}/proposed-slide.png"
    prompt = read_prompt(args)

    args.db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(args.db) as conn:
        conn.executescript(SCHEMA)
        conn.execute(
            """
            INSERT INTO candidates(
                id, batch_id, target_path, topic_path, slide_ref, brief, prompt,
                candidate_url, current_slide_url, proposed_slide_url, candidate_rel_path,
                status, review_comment, reviewed_by, reviewed_at, processed_at, requeued_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', '', NULL, NULL, NULL, NULL, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                batch_id = excluded.batch_id,
                target_path = excluded.target_path,
                topic_path = excluded.topic_path,
                slide_ref = excluded.slide_ref,
                brief = excluded.brief,
                prompt = excluded.prompt,
                candidate_url = excluded.candidate_url,
                current_slide_url = excluded.current_slide_url,
                proposed_slide_url = excluded.proposed_slide_url,
                candidate_rel_path = excluded.candidate_rel_path,
                status = 'pending',
                review_comment = '',
                reviewed_by = NULL,
                reviewed_at = NULL,
                processed_at = NULL,
                requeued_at = NULL,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                candidate_id,
                args.batch_id,
                args.target_path,
                args.topic_path,
                args.slide_ref,
                args.brief,
                prompt,
                candidate_url,
                current_slide_url,
                proposed_slide_url,
                candidate_rel_path,
            ),
        )
        conn.execute(
            """
            INSERT INTO review_events(candidate_id, actor, action, comment)
            VALUES (?, 'image-review-register', 'registered', ?)
            """,
            (candidate_id, f"{args.batch_id}: {args.brief}"),
        )

    batch_file = args.batch_file or Path("image-review/batches") / f"{args.batch_id}.md"
    append_batch_row(
        batch_file,
        {
            "id": candidate_id,
            "target_path": args.target_path,
            "slide_ref": args.slide_ref,
            "brief": args.brief,
        },
        args.review_base_url,
    )

    print(candidate_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
