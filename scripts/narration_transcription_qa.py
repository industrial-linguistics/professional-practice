#!/usr/bin/env python3
"""Transcribe course narration and compare it with the authored scripts."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from faster_whisper import WhisperModel


WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
SPEAKER_RE = re.compile(r"^\s*Speaker\s+\d+\s*:\s*", re.IGNORECASE)


@dataclass
class TopicResult:
    topic: str
    audio_path: str
    duration_seconds: float
    reference_words: int
    transcript_words: int
    substitutions: int
    deletions: int
    insertions: int
    word_error_rate: float
    real_time_factor: float
    review_priority: str
    transcript_path: str
    segments_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--content-root",
        type=Path,
        default=Path("content/part-01"),
        help="Directory whose immediate children contain audio.mp3 and narratives/",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--cpu-threads", type=int, default=10)
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument(
        "--topic",
        action="append",
        help="Limit the run to this topic directory; repeat for multiple topics",
    )
    parser.add_argument(
        "--vad-filter",
        action="store_true",
        help="Use voice-activity detection to suppress silence-driven hallucinations",
    )
    parser.add_argument(
        "--no-condition-on-previous-text",
        action="store_false",
        dest="condition_on_previous_text",
        help="Decode each window independently",
    )
    parser.set_defaults(condition_on_previous_text=True)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalise_words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower().replace("’", "'").replace("—", " "))


def read_reference(topic_dir: Path) -> str:
    narrative_dir = topic_dir / "narratives"
    files = sorted(
        path
        for path in narrative_dir.glob("*.md")
        if not path.name.startswith(("_", "."))
    )
    paragraphs: list[str] = []
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = SPEAKER_RE.sub("", line.strip())
            if line and not line.startswith("#"):
                paragraphs.append(line)
    return "\n".join(paragraphs)


def edit_counts(reference: list[str], hypothesis: list[str]) -> tuple[int, int, int]:
    """Return substitutions, deletions and insertions for a word-level alignment."""
    rows = len(reference) + 1
    cols = len(hypothesis) + 1
    distance = [[0] * cols for _ in range(rows)]
    operation = [[""] * cols for _ in range(rows)]
    for row in range(1, rows):
        distance[row][0] = row
        operation[row][0] = "D"
    for col in range(1, cols):
        distance[0][col] = col
        operation[0][col] = "I"

    for row in range(1, rows):
        for col in range(1, cols):
            if reference[row - 1] == hypothesis[col - 1]:
                distance[row][col] = distance[row - 1][col - 1]
                operation[row][col] = "M"
                continue
            candidates = (
                (distance[row - 1][col - 1] + 1, "S"),
                (distance[row - 1][col] + 1, "D"),
                (distance[row][col - 1] + 1, "I"),
            )
            distance[row][col], operation[row][col] = min(candidates)

    substitutions = deletions = insertions = 0
    row, col = len(reference), len(hypothesis)
    while row or col:
        op = operation[row][col]
        if op in {"M", "S"}:
            substitutions += op == "S"
            row -= 1
            col -= 1
        elif op == "D":
            deletions += 1
            row -= 1
        elif op == "I":
            insertions += 1
            col -= 1
        else:
            raise RuntimeError(f"Invalid alignment state at {row}, {col}")
    return substitutions, deletions, insertions


def priority_for(wer: float, reference_words: int, transcript_words: int) -> str:
    if transcript_words == 0 or wer >= 0.20:
        return "urgent"
    if wer >= 0.10 or transcript_words < reference_words * 0.85:
        return "review"
    return "pass"


def write_status(
    output_dir: Path,
    *,
    state: str,
    completed: int,
    total: int,
    current_topic: str | None,
    started_at: str,
    error: str | None = None,
) -> None:
    payload = {
        "state": state,
        "completed": completed,
        "total": total,
        "current_topic": current_topic,
        "started_at": started_at,
        "updated_at": utc_now(),
    }
    if error:
        payload["error"] = error
    (output_dir / "status.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def write_reports(
    output_dir: Path, model_name: str, results: list[TopicResult]
) -> None:
    result_payload = {
        "generated_at": utc_now(),
        "model": model_name,
        "topics": [asdict(result) for result in results],
    }
    (output_dir / "results.json").write_text(
        json.dumps(result_payload, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Narration transcription QA",
        "",
        f"- Model: `{model_name}`",
        f"- Topics: {len(results)}",
        "- Priority thresholds: pass <10% WER; review 10–20%; urgent ≥20% or empty",
        "",
        "| Topic | Duration | Reference words | Transcript words | WER | RTF | Priority |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result.topic} | {result.duration_seconds:.1f}s | "
            f"{result.reference_words} | {result.transcript_words} | "
            f"{result.word_error_rate:.1%} | {result.real_time_factor:.2f} | "
            f"{result.review_priority} |"
        )
    lines.extend(
        [
            "",
            "Word error rate is a screening signal, not a substitute for listening.",
            "Review transcript and segment files for every item marked review or urgent.",
            "",
        ]
    )
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    content_root = args.content_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()

    topic_dirs = sorted(
        path
        for path in content_root.iterdir()
        if path.is_dir()
        and (path / "audio.mp3").is_file()
        and (path / "narratives").is_dir()
        and (not args.topic or path.name in args.topic)
    )
    if not topic_dirs:
        print(f"No narration topics found under {content_root}", file=sys.stderr)
        return 2

    write_status(
        output_dir,
        state="loading_model",
        completed=0,
        total=len(topic_dirs),
        current_topic=None,
        started_at=started_at,
    )
    print(f"[{utc_now()}] loading model {args.model}", flush=True)
    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type="int8",
        cpu_threads=args.cpu_threads,
        num_workers=1,
    )

    results: list[TopicResult] = []
    try:
        for index, topic_dir in enumerate(topic_dirs):
            topic = topic_dir.name
            write_status(
                output_dir,
                state="transcribing",
                completed=index,
                total=len(topic_dirs),
                current_topic=topic,
                started_at=started_at,
            )
            print(
                f"[{utc_now()}] {index + 1}/{len(topic_dirs)} transcribing {topic}",
                flush=True,
            )

            reference = read_reference(topic_dir)
            reference_words = normalise_words(reference)
            topic_output = output_dir / topic
            topic_output.mkdir(parents=True, exist_ok=True)
            (topic_output / "reference.txt").write_text(
                reference + "\n", encoding="utf-8"
            )

            start = time.monotonic()
            segments_iter, info = model.transcribe(
                str(topic_dir / "audio.mp3"),
                language="en",
                beam_size=args.beam_size,
                vad_filter=args.vad_filter,
                condition_on_previous_text=args.condition_on_previous_text,
            )
            segment_rows = []
            transcript_parts = []
            for segment in segments_iter:
                text = segment.text.strip()
                transcript_parts.append(text)
                segment_rows.append(
                    {
                        "start": round(segment.start, 3),
                        "end": round(segment.end, 3),
                        "text": text,
                        "avg_logprob": segment.avg_logprob,
                        "no_speech_prob": segment.no_speech_prob,
                    }
                )
            elapsed = time.monotonic() - start
            transcript = " ".join(transcript_parts).strip()
            transcript_words = normalise_words(transcript)
            substitutions, deletions, insertions = edit_counts(
                reference_words, transcript_words
            )
            errors = substitutions + deletions + insertions
            wer = errors / max(1, len(reference_words))
            duration = float(info.duration)
            priority = priority_for(wer, len(reference_words), len(transcript_words))

            transcript_path = topic_output / "transcript.txt"
            segments_path = topic_output / "segments.json"
            transcript_path.write_text(transcript + "\n", encoding="utf-8")
            segments_path.write_text(
                json.dumps(segment_rows, indent=2) + "\n", encoding="utf-8"
            )
            result = TopicResult(
                topic=topic,
                audio_path=str(topic_dir / "audio.mp3"),
                duration_seconds=duration,
                reference_words=len(reference_words),
                transcript_words=len(transcript_words),
                substitutions=substitutions,
                deletions=deletions,
                insertions=insertions,
                word_error_rate=wer,
                real_time_factor=elapsed / max(duration, 0.001),
                review_priority=priority,
                transcript_path=str(transcript_path),
                segments_path=str(segments_path),
            )
            results.append(result)
            write_reports(output_dir, args.model, results)
            print(
                f"[{utc_now()}] completed {topic}: WER={wer:.1%}, "
                f"priority={priority}, RTF={result.real_time_factor:.2f}",
                flush=True,
            )

        write_status(
            output_dir,
            state="completed",
            completed=len(results),
            total=len(topic_dirs),
            current_topic=None,
            started_at=started_at,
        )
        print(f"[{utc_now()}] all topics completed", flush=True)
        return 0
    except Exception as exc:
        write_status(
            output_dir,
            state="failed",
            completed=len(results),
            total=len(topic_dirs),
            current_topic=topic_dirs[len(results)].name
            if len(results) < len(topic_dirs)
            else None,
            started_at=started_at,
            error=f"{type(exc).__name__}: {exc}",
        )
        raise


if __name__ == "__main__":
    raise SystemExit(main())
