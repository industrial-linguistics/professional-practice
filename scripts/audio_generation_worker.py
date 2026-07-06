#!/usr/bin/env python3
"""Bounded audio/video generation worker for the raksasa cron job."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_manifest import BuildManifest  # noqa: E402
from validate_content import validate_content_structure  # noqa: E402


DEFAULT_STATE_FILE = Path("state/audio-worker-state.json")
DEFAULT_LOG_DIR = Path("logs/audio-generation")
ELEVENLABS_SUBSCRIPTION_URL = "https://api.elevenlabs.io/v1/user/subscription"


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name, "")
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_utc(value: object) -> datetime | None:
    if not value:
        return None
    try:
        text = str(value).replace("Z", "+00:00")
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


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
            if (topic_dir / "slides.html").exists():
                topics.append(topic_dir)
    return topics


def topic_input_chars(topic_path: Path) -> int:
    narratives = topic_path / "narratives"
    total = 0
    for narrative in sorted(narratives.glob("*.md")):
        total += len(narrative.read_text())
    return total


def read_api_key() -> tuple[str, str]:
    env_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if env_key:
        return env_key, "ELEVENLABS_API_KEY"
    key_file = Path.home() / ".elevenlabs.mq.io"
    if key_file.exists():
        key = key_file.read_text().strip()
        if key:
            return key, str(key_file)
    return "", ""


def fetch_account_character_count(api_key: str) -> tuple[dict, str]:
    request = urllib.request.Request(
        ELEVENLABS_SUBSCRIPTION_URL,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:500]
        return {}, f"http_{error.code}: {detail}"
    except Exception as error:  # pragma: no cover - runtime network state
        return {}, f"request_failed: {error}"

    try:
        count = int(float(payload.get("character_count", 0)))
    except (TypeError, ValueError):
        count = 0
    try:
        limit = int(float(payload.get("character_limit", 0)))
    except (TypeError, ValueError):
        limit = 0
    payload["_character_count_int"] = count
    payload["_character_limit_int"] = limit
    return payload, ""


def audio_mtime(topic_path: Path) -> datetime | None:
    audio = topic_path / "audio.wav"
    if not audio.exists():
        return None
    return datetime.fromtimestamp(audio.stat().st_mtime, timezone.utc)


def project_usage_estimate(state: dict, all_topics: list[Path], now: datetime) -> dict:
    today = now.date()
    month = now.strftime("%Y-%m")
    daily = 0
    monthly = 0
    counted_day_keys: set[tuple[str, str]] = set()
    counted_month_keys: set[tuple[str, str]] = set()

    for event in state.get("usage_events", []):
        event_time = parse_utc(event.get("event_time"))
        if not event_time:
            continue
        try:
            chars = int(event.get("estimated_chars", 0))
        except (TypeError, ValueError):
            chars = 0
        topic_key = str(event.get("topic", ""))
        if event_time.date() == today:
            daily += chars
            counted_day_keys.add((topic_key, str(today)))
        if event_time.strftime("%Y-%m") == month:
            monthly += chars
            counted_month_keys.add((topic_key, month))

    # Seed the estimate from existing outputs created before explicit usage
    # events were added. This is conservative and keeps the newly enabled cron
    # from spending the rest of today's quota after manual bootstrap renders.
    for topic_path in all_topics:
        topic_key = str(topic_path)
        built_at = audio_mtime(topic_path)
        if built_at is None:
            entry = state.get("topics", {}).get(topic_key, {})
            built_at = parse_utc(entry.get("last_built_at"))
        if built_at is None:
            continue
        chars = topic_input_chars(topic_path)
        if built_at.date() == today and (topic_key, str(today)) not in counted_day_keys:
            daily += chars
        if built_at.strftime("%Y-%m") == month and (topic_key, month) not in counted_month_keys:
            monthly += chars

    return {
        "daily_estimated_chars": daily,
        "monthly_estimated_chars": monthly,
    }


def budget_snapshot(
    state: dict,
    all_topics: list[Path],
    *,
    daily_limit: int,
    monthly_limit: int,
    account_period_limit: int,
) -> dict:
    now = datetime.now(timezone.utc)
    project_usage = project_usage_estimate(state, all_topics, now)
    remaining: list[int] = []
    snapshot = {
        **project_usage,
        "daily_char_limit": daily_limit,
        "monthly_char_limit": monthly_limit,
        "account_period_char_limit": account_period_limit,
        "account_status": "not_checked",
    }

    if daily_limit > 0:
        remaining.append(daily_limit - project_usage["daily_estimated_chars"])
    if monthly_limit > 0:
        remaining.append(monthly_limit - project_usage["monthly_estimated_chars"])

    if account_period_limit > 0:
        api_key, key_source = read_api_key()
        snapshot["account_key_source"] = key_source
        if not api_key:
            snapshot["account_status"] = "missing_api_key"
            remaining.append(0)
        else:
            account, error = fetch_account_character_count(api_key)
            if error:
                snapshot["account_status"] = error
                remaining.append(0)
            else:
                count = account.get("_character_count_int", 0)
                real_limit = account.get("_character_limit_int", 0)
                snapshot.update(
                    {
                        "account_status": "ok",
                        "account_character_count": count,
                        "account_reported_character_limit": real_limit,
                        "account_remaining_characters": max(real_limit - count, 0),
                        "account_next_reset_unix": account.get(
                            "next_character_count_reset_unix", ""
                        ),
                    }
                )
                remaining.append(account_period_limit - count)

    snapshot["remaining_estimated_chars"] = max(min(remaining), 0) if remaining else None
    return snapshot


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
    remaining_chars: int | None,
) -> tuple[list[tuple[Path, str, str, int]], int, int]:
    selected: list[tuple[Path, str, str, int]] = []
    blocked_count = 0
    budget_wait_count = 0
    topics_state = state.setdefault("topics", {})
    budget_left = remaining_chars

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
        estimated_chars = topic_input_chars(topic_path)
        if not validation.passed:
            blocked_count += 1
            topics_state[topic_key] = {
                **topics_state.get(topic_key, {}),
                "status": "blocked-content",
                "source_fingerprint": source_id,
                "estimated_chars": estimated_chars,
                "last_checked_at": utc_now(),
                "last_error": validation.message,
            }
            continue

        if budget_left is not None and estimated_chars > budget_left:
            budget_wait_count += 1
            topics_state[topic_key] = {
                **topics_state.get(topic_key, {}),
                "status": "budget-wait",
                "source_fingerprint": source_id,
                "estimated_chars": estimated_chars,
                "last_checked_at": utc_now(),
                "last_budget_reason": (
                    f"estimated {estimated_chars} chars exceeds remaining "
                    f"daily/monthly/account budget {budget_left}"
                ),
            }
            continue

        selected.append((topic_path, reason or "needs rebuild", source_id, estimated_chars))
        if budget_left is not None:
            budget_left -= estimated_chars
        if len(selected) >= max_topics:
            break

    return selected, blocked_count, budget_wait_count


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
    parser.add_argument(
        "--daily-char-limit",
        type=int,
        default=env_int("AUDIO_WORKER_DAILY_CHAR_LIMIT", 10000),
        help="Estimated Professional Practice characters allowed per UTC day; 0 disables.",
    )
    parser.add_argument(
        "--monthly-char-limit",
        type=int,
        default=env_int("AUDIO_WORKER_MONTHLY_CHAR_LIMIT", 250000),
        help="Estimated Professional Practice characters allowed per UTC month; 0 disables.",
    )
    parser.add_argument(
        "--account-period-char-limit",
        type=int,
        default=env_int("AUDIO_WORKER_ACCOUNT_PERIOD_CHAR_LIMIT", 500000),
        help=(
            "Shared ElevenLabs period character cap; defaults to base quota so "
            "rollovers are preserved as reserve. 0 disables."
        ),
    )
    args = parser.parse_args()

    os.chdir(REPO_ROOT)
    content_dir = Path(args.content_dir)
    state_file = Path(args.state_file)
    log_dir = Path(args.log_dir)
    state = load_state(state_file)
    manifest = BuildManifest()

    all_topics = topic_dirs(content_dir)
    budget = budget_snapshot(
        state,
        all_topics,
        daily_limit=args.daily_char_limit,
        monthly_limit=args.monthly_char_limit,
        account_period_limit=args.account_period_char_limit,
    )
    remaining_chars = budget.get("remaining_estimated_chars")

    selected, blocked_count, budget_wait_count = select_topics(
        all_topics,
        manifest,
        state,
        max(1, args.max_topics),
        remaining_chars,
    )

    run_record = {
        "started_at": utc_now(),
        "max_topics": max(1, args.max_topics),
        "selected": [str(topic) for topic, _, _, _ in selected],
        "blocked_count": blocked_count,
        "budget_wait_count": budget_wait_count,
        "budget": budget,
        "results": [],
    }

    if not selected:
        print(
            f"No valid topics need audio/video generation "
            f"({blocked_count} content-blocked topic(s), "
            f"{budget_wait_count} budget-wait topic(s))."
        )
        if budget.get("remaining_estimated_chars") == 0:
            print(f"Budget guard active: {json.dumps(budget, sort_keys=True)}")
        run_record["finished_at"] = utc_now()
        state.setdefault("runs", []).append(run_record)
        state["runs"] = state["runs"][-50:]
        save_state(state_file, state)
        return 0

    if args.dry_run:
        for topic_path, reason, _, estimated_chars in selected:
            print(f"Would build {topic_path}: {reason} ({estimated_chars} estimated chars)")
        run_record["dry_run"] = True
        run_record["finished_at"] = utc_now()
        state.setdefault("runs", []).append(run_record)
        state["runs"] = state["runs"][-50:]
        save_state(state_file, state)
        return 0

    exit_code = 0
    for topic_path, reason, source_id, estimated_chars in selected:
        topic_key = str(topic_path)
        print(f"Building {topic_key}: {reason} ({estimated_chars} estimated chars)")
        ok, log_path = run_topic(topic_path, log_dir)
        entry = state.setdefault("topics", {}).get(topic_key, {})
        event_time = utc_now()
        if ok:
            state["topics"][topic_key] = {
                **entry,
                "status": "built",
                "source_fingerprint": source_id,
                "estimated_chars": estimated_chars,
                "last_built_at": event_time,
                "last_log": str(log_path),
                "last_error": "",
            }
            state.setdefault("usage_events", []).append(
                {
                    "event_time": event_time,
                    "project_name": "professional-practice",
                    "topic": topic_key,
                    "operation": "audio-video-build",
                    "estimated_chars": estimated_chars,
                    "evidence": {"log": str(log_path)},
                }
            )
            state["usage_events"] = state["usage_events"][-500:]
            print(f"Built {topic_key}; log: {log_path}")
        else:
            state["topics"][topic_key] = {
                **entry,
                "status": "failed",
                "source_fingerprint": source_id,
                "estimated_chars": estimated_chars,
                "last_failed_at": event_time,
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
                "estimated_chars": estimated_chars,
            }
        )

    run_record["finished_at"] = utc_now()
    state.setdefault("runs", []).append(run_record)
    state["runs"] = state["runs"][-50:]
    save_state(state_file, state)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
