#!/usr/bin/env python3
"""Record provenance only after generating and validating a narration master."""

import argparse
import json
from pathlib import Path

from course_content import media_provenance, narration_fingerprint


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", type=Path)
    parser.add_argument("--expected-fingerprint")
    args = parser.parse_args()
    fingerprint = narration_fingerprint(args.topic)
    if args.expected_fingerprint is None:
        print(fingerprint)
        return
    if fingerprint != args.expected_fingerprint:
        raise SystemExit("Narration changed during audio generation; do not publish this take")
    audio = args.topic / "audio.wav"
    subtitles = args.topic / "subtitles.vtt"
    payload = media_provenance(args.topic, audio, subtitles)
    destination = args.topic / "audio-source.json"
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n")
    temporary.replace(destination)


if __name__ == "__main__":
    main()
