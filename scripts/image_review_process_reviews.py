#!/usr/bin/env python3
"""Process image-review decisions pulled back from merah."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sqlite3
from pathlib import Path


DEFAULT_DB = Path("state/image-review/image-review.sqlite")
DEFAULT_CANDIDATES = Path("state/image-review/candidates")
DEFAULT_REWORK = Path("image-review/rework-queue.md")


def repo_path(root: Path, rel_path: str) -> Path:
    target = (root / rel_path).resolve()
    root = root.resolve()
    if root != target and root not in target.parents:
        raise ValueError(f"path escapes repository root: {rel_path}")
    return target


def candidate_path(candidates_dir: Path, rel_path: str, candidate_url: str) -> Path:
    rel = rel_path.strip()
    prefix = "/image-review/candidates/"
    if not rel and candidate_url.startswith(prefix):
        rel = candidate_url[len(prefix) :]
    return candidates_dir / rel


def ensure_rework_file(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Image rework queue\n\n"
        "Rejected and commented image candidates are appended here by the raksasa review processor.\n\n",
        encoding="utf-8",
    )


def append_rework(path: Path, row: sqlite3.Row) -> None:
    ensure_rework_file(path)
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    comment = row["review_comment"].strip() or "(no comment supplied)"
    prompt = row["prompt"].strip() or "(no prompt recorded)"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"## {row['id']}\n\n"
            f"- Requeued: {now}\n"
            f"- Status: {row['status']}\n"
            f"- Target: `{row['target_path']}`\n"
            f"- Slide: {row['slide_ref'] or '-'}\n"
            f"- Reviewer: {row['reviewed_by'] or 'unknown'} at {row['reviewed_at'] or '-'}\n"
            f"- Comment: {comment}\n\n"
            f"Original prompt/spec:\n\n```text\n{prompt}\n```\n\n"
        )


def process_approvals(
    conn: sqlite3.Connection,
    repo_root: Path,
    candidates_dir: Path,
    dry_run: bool,
) -> int:
    rows = conn.execute(
        """
        SELECT id, target_path, candidate_rel_path, candidate_url
        FROM candidates
        WHERE status = 'approved' AND processed_at IS NULL
        ORDER BY reviewed_at, id
        """
    ).fetchall()

    processed = 0
    for row in rows:
        src = candidate_path(candidates_dir, row["candidate_rel_path"], row["candidate_url"])
        dest = repo_path(repo_root, row["target_path"])
        if not src.exists():
            print(f"missing approved candidate image for {row['id']}: {src}")
            continue
        print(f"approve {row['id']}: {src} -> {dest}")
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            conn.execute(
                """
                UPDATE candidates
                SET status = 'processed',
                    processed_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (row["id"],),
            )
            conn.execute(
                """
                INSERT INTO review_events(candidate_id, actor, action, comment)
                VALUES (?, 'image-review-process', 'processed', ?)
                """,
                (row["id"], f"installed {row['target_path']}"),
            )
        processed += 1
    return processed


def process_rework(
    conn: sqlite3.Connection,
    rework_file: Path,
    dry_run: bool,
) -> int:
    rows = conn.execute(
        """
        SELECT id, status, target_path, slide_ref, prompt, review_comment, reviewed_by, reviewed_at
        FROM candidates
        WHERE status IN ('rejected', 'commented') AND requeued_at IS NULL
        ORDER BY reviewed_at, id
        """
    ).fetchall()

    processed = 0
    for row in rows:
        print(f"requeue {row['id']}: {row['status']}")
        if not dry_run:
            append_rework(rework_file, row)
            conn.execute(
                """
                UPDATE candidates
                SET requeued_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (row["id"],),
            )
            conn.execute(
                """
                INSERT INTO review_events(candidate_id, actor, action, comment)
                VALUES (?, 'image-review-process', 'requeued', ?)
                """,
                (row["id"], row["status"]),
            )
        processed += 1
    return processed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--candidates-dir", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--rework-file", type=Path, default=DEFAULT_REWORK)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"no review database found at {args.db}")
        return 0

    with sqlite3.connect(args.db) as conn:
        conn.row_factory = sqlite3.Row
        approvals = process_approvals(conn, args.repo_root, args.candidates_dir, args.dry_run)
        reworks = process_rework(conn, args.rework_file, args.dry_run)
        if not args.dry_run:
            conn.commit()

    print(f"processed approvals={approvals} rework={reworks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
