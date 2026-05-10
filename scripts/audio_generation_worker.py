#!/usr/bin/env python3
"""Bounded audio/video generation worker for the raksasa cron job."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_manifest import BuildManifest  # noqa: E402
from validate_content import validate_content_structure  # noqa: E402


DEFAULT_STATE_FILE = Path("state/audio-worker-state.json")
DEFAULT_LOG_DIR = Path("logs/audio-generation")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"topics": {}, "runs": []}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {"topics": {}, "runs": []}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def source_fingerprint(manifest: BuildManifest, topic_path: Path) -> str:
    hashes = manifest.get_source_hashes(topic_path)
    payload = json.dumps(hashes, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def topic_dirs(content_dir: Path) -> list[Path]:
    topics: list[Path] = []
    for part_dir in sorted(content_dir.glob("part-*")):
        if not part_dir.is_dir():
            continue
        for topic_dir in sorted(part_dir.iterdir()):
            if (topic_dir / "slides.md").exists():
                topics.append(topic_dir)
    return topics


def tail(path: Path, lines: int = 40) -> str:
    if not path.exists():
        return ""
    data = path.read_text(errors="replace").splitlines()
    return "\n".join(data[-lines:])


def run_topic(topic_path: Path, log_dir: Path) -> tuple[bool, Path]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_topic = str(topic_path).replace("/", "__")
    log_path = log_dir / f"{timestamp}-{safe_topic}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["bash", "scripts/build_videos.sh", str(topic_path)]
    with log_path.open("w") as log:
        log.write(f"$ {' '.join(cmd)}\n")
        log.flush()
        result = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=os.environ.copy(),
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
    return result.returncode == 0, log_path


def select_topics(
    all_topics: list[Path],
    manifest: BuildManifest,
    state: dict,
    max_topics: int,
) -> tuple[list[tuple[Path, str, str]], int]:
    selected: list[tuple[Path, str, str]] = []
    blocked_count = 0
    topics_state = state.setdefault("topics", {})

    for topic_path in all_topics:
        topic_key = str(topic_path)
        source_id = source_fingerprint(manifest, topic_path)
        needs_rebuild, reason = manifest.needs_rebuild(topic_path)
        if not needs_rebuild:
            topics_state[topic_key] = {
                **topics_state.get(topic_key, {}),
                "status": "up-to-date",
                "source_fingerprint": source_id,
                "last_checked_at": utc_now(),
            }
            continue

        validation = validate_content_structure(topic_path)
        if not validation.passed:
            blocked_count += 1
            topics_state[topic_key] = {
                **topics_state.get(topic_key, {}),
                "status": "blocked-content",
                "source_fingerprint": source_id,
                "last_checked_at": utc_now(),
                "last_error": validation.message,
            }
            continue

        selected.append((topic_path, reason or "needs rebuild", source_id))
        if len(selected) >= max_topics:
            break

    return selected, blocked_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content-dir",
        default="content",
        help="Content directory to scan.",
    )
    parser.add_argument(
        "--max-topics",
        type=int,
        default=int(os.environ.get("AUDIO_WORKER_MAX_TOPICS", "1")),
        help="Maximum valid topics to build in this run.",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=DEFAULT_STATE_FILE,
        help="Worker state file.",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=DEFAULT_LOG_DIR,
        help="Per-topic build log directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Select topics and update blocked/up-to-date state without building.",
    )
    args = parser.parse_args()

    os.chdir(REPO_ROOT)
    content_dir = Path(args.content_dir)
    state_file = Path(args.state_file)
    log_dir = Path(args.log_dir)
    state = load_state(state_file)
    manifest = BuildManifest()

    all_topics = topic_dirs(content_dir)
    selected, blocked_count = select_topics(
        all_topics,
        manifest,
        state,
        max(1, args.max_topics),
    )

    run_record = {
        "started_at": utc_now(),
        "max_topics": max(1, args.max_topics),
        "selected": [str(topic) for topic, _, _ in selected],
        "blocked_count": blocked_count,
        "results": [],
    }

    if not selected:
        print(
            f"No valid topics need audio/video generation "
            f"({blocked_count} content-blocked topic(s))."
        )
        run_record["finished_at"] = utc_now()
        state.setdefault("runs", []).append(run_record)
        state["runs"] = state["runs"][-50:]
        save_state(state_file, state)
        return 0

    if args.dry_run:
        for topic_path, reason, _ in selected:
            print(f"Would build {topic_path}: {reason}")
        run_record["dry_run"] = True
        run_record["finished_at"] = utc_now()
        state.setdefault("runs", []).append(run_record)
        state["runs"] = state["runs"][-50:]
        save_state(state_file, state)
        return 0

    exit_code = 0
    for topic_path, reason, source_id in selected:
        topic_key = str(topic_path)
        print(f"Building {topic_key}: {reason}")
        ok, log_path = run_topic(topic_path, log_dir)
        entry = state.setdefault("topics", {}).get(topic_key, {})
        if ok:
            state["topics"][topic_key] = {
                **entry,
                "status": "built",
                "source_fingerprint": source_id,
                "last_built_at": utc_now(),
                "last_log": str(log_path),
                "last_error": "",
            }
            print(f"Built {topic_key}; log: {log_path}")
        else:
            state["topics"][topic_key] = {
                **entry,
                "status": "failed",
                "source_fingerprint": source_id,
                "last_failed_at": utc_now(),
                "last_log": str(log_path),
                "last_error": tail(log_path),
            }
            print(f"Failed {topic_key}; log: {log_path}", file=sys.stderr)
            exit_code = 1

        run_record["results"].append(
            {
                "topic": topic_key,
                "status": "built" if ok else "failed",
                "log": str(log_path),
            }
        )

    run_record["finished_at"] = utc_now()
    state.setdefault("runs", []).append(run_record)
    state["runs"] = state["runs"][-50:]
    save_state(state_file, state)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
