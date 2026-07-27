#!/usr/bin/env python3
"""Build every paperback and Kindle release asset, then validate the result."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KINDLE_PREVIEWER = Path(
    "/Applications/Kindle Previewer 3.app/Contents/MacOS/Kindle Previewer 3"
)
KINDLE_AUDIT = ROOT / "textbook" / "audit" / "kindle-previewer"


def run(*command: str) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    run(sys.executable, "scripts/validate_textbook_sources.py", "--strict")
    run(sys.executable, "scripts/build_textbook.py")
    run(sys.executable, "scripts/build_kdp_cover.py")
    run(sys.executable, "scripts/build_textbook_epub.py")
    if KINDLE_PREVIEWER.exists():
        shutil.rmtree(KINDLE_AUDIT, ignore_errors=True)
        KINDLE_AUDIT.mkdir(parents=True)
        run(
            str(KINDLE_PREVIEWER),
            "textbook/it-professional-practice.epub",
            "-convert",
            "-qualitychecks",
            "-output",
            str(KINDLE_AUDIT),
            "-locale",
            "en",
        )
    else:
        raise SystemExit("Kindle Previewer 3 is required for a release build.")
    run(sys.executable, "scripts/validate_textbook_release.py")
    print("Built and validated the complete textbook release candidate.")


if __name__ == "__main__":
    main()
