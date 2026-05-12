#!/usr/bin/env python3
"""Validate generated narration audio against the source script.

The script expects a speech-recognition command to be available. By default it
tries the common `whisper` CLI; alternatively set AUDIO_TRANSCRIPT_COMMAND or
pass --asr-command. Custom commands may write the transcript to stdout, or use
{audio} and {transcript} placeholders to receive explicit paths.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SPEAKER_RE = re.compile(r"^\s*Speaker\s+\d+\s*:\s*(.*)$", re.IGNORECASE)
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
MARKDOWN_RE = re.compile(r"[*_`#]")
ITIL_RE = re.compile(r"\bITIL\b", re.IGNORECASE)
TOKEN_RE = re.compile(r"[a-z0-9]+")
FORBIDDEN_TRANSCRIPT_PHRASES = {
    "speaker 1",
    "speaker one",
    "speaker 2",
    "speaker two",
}


def clean_script_text(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = MARKDOWN_RE.sub("", text)
    parts: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = SPEAKER_RE.match(line)
        if match:
            line = match.group(1).strip()
        line = ITIL_RE.sub("eye till", line)
        if line:
            parts.append(line)
    return " ".join(parts)


def expected_script(topic_path: Path) -> str:
    narratives = topic_path / "narratives"
    if not narratives.exists():
        raise SystemExit(f"narratives directory not found: {narratives}")
    texts = [clean_script_text(path.read_text(encoding="utf-8")) for path in sorted(narratives.glob("*.md"))]
    return " ".join(text for text in texts if text)


def normalize_tokens(text: str) -> list[str]:
    text = text.lower().replace("-", " ")
    text = ITIL_RE.sub("eye till", text)
    return TOKEN_RE.findall(text)


def word_error_rate(reference: list[str], hypothesis: list[str]) -> float:
    if not reference:
        return 1.0 if hypothesis else 0.0
    previous = list(range(len(hypothesis) + 1))
    for i, ref_token in enumerate(reference, start=1):
        current = [i]
        for j, hyp_token in enumerate(hypothesis, start=1):
            substitution = previous[j - 1] + (0 if ref_token == hyp_token else 1)
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            current.append(min(substitution, insertion, deletion))
        previous = current
    return previous[-1] / len(reference)


def run_custom_asr(command: str, audio_path: Path) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        transcript_path = Path(tmpdir) / "transcript.txt"
        if "{audio}" in command or "{transcript}" in command:
            rendered = command.format(
                audio=shlex.quote(str(audio_path)),
                transcript=shlex.quote(str(transcript_path)),
            )
            result = subprocess.run(rendered, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(
                shlex.split(command) + [str(audio_path)],
                capture_output=True,
                text=True,
            )
        if result.returncode != 0:
            raise SystemExit(result.stderr.strip() or f"ASR command failed with exit code {result.returncode}")
        if transcript_path.exists():
            return transcript_path.read_text(encoding="utf-8")
        return result.stdout


def run_whisper(audio_path: Path, model: str) -> str:
    whisper = shutil.which("whisper")
    if not whisper:
        raise SystemExit(
            "No ASR command found. Install the whisper CLI, set AUDIO_TRANSCRIPT_COMMAND, "
            "or pass --transcript-file."
        )
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            whisper,
            str(audio_path),
            "--language",
            "en",
            "--model",
            model,
            "--output_format",
            "txt",
            "--output_dir",
            tmpdir,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(result.stderr.strip() or f"whisper failed with exit code {result.returncode}")
        transcript_path = Path(tmpdir) / f"{audio_path.stem}.txt"
        if not transcript_path.exists():
            raise SystemExit("whisper completed but did not write a transcript")
        return transcript_path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic_path", type=Path)
    parser.add_argument("--audio", type=Path, help="Audio file to validate; defaults to <topic>/audio.wav")
    parser.add_argument("--transcript-file", type=Path, help="Use an existing transcript instead of running ASR")
    parser.add_argument("--asr-command", default=os.environ.get("AUDIO_TRANSCRIPT_COMMAND", ""))
    parser.add_argument("--whisper-model", default=os.environ.get("AUDIO_TRANSCRIPT_WHISPER_MODEL", "base"))
    parser.add_argument("--max-wer", type=float, default=float(os.environ.get("AUDIO_TRANSCRIPT_MAX_WER", "0.25")))
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    topic_path = args.topic_path
    audio_path = args.audio or topic_path / "audio.wav"
    if not audio_path.exists():
        raise SystemExit(f"audio file not found: {audio_path}")

    expected = expected_script(topic_path)
    if args.transcript_file:
        transcript = args.transcript_file.read_text(encoding="utf-8")
    elif args.asr_command:
        transcript = run_custom_asr(args.asr_command, audio_path)
    else:
        transcript = run_whisper(audio_path, args.whisper_model)

    expected_tokens = normalize_tokens(expected)
    transcript_tokens = normalize_tokens(transcript)
    wer = word_error_rate(expected_tokens, transcript_tokens)
    transcript_normalized = " ".join(transcript_tokens)
    forbidden = sorted(
        phrase for phrase in FORBIDDEN_TRANSCRIPT_PHRASES if phrase in transcript_normalized
    )
    passed = wer <= args.max_wer and not forbidden

    result = {
        "topic": str(topic_path),
        "audio": str(audio_path),
        "expected_words": len(expected_tokens),
        "transcript_words": len(transcript_tokens),
        "word_error_rate": round(wer, 4),
        "max_word_error_rate": args.max_wer,
        "forbidden_phrases": forbidden,
        "passed": passed,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        status = "PASS" if passed else "FAIL"
        print(
            f"{status} audio transcript validation for {topic_path}: "
            f"WER={wer:.3f}, expected_words={len(expected_tokens)}, "
            f"transcript_words={len(transcript_tokens)}"
        )
        if forbidden:
            print(f"Forbidden spoken labels detected: {', '.join(forbidden)}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
