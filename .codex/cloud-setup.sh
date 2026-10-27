#!/usr/bin/env bash
# Install the image producer's Linux tools without audio-provider credentials.
set -euo pipefail
cd "$(dirname "$0")/.."
ADMIN=()
if [[ $(id -u) -ne 0 ]]; then ADMIN=(sudo); fi
"${ADMIN[@]}" apt-get update
"${ADMIN[@]}" apt-get install -y python3 python3-venv python3-pip sqlite3 graphviz nodejs npm \
  ffmpeg poppler-utils fonts-dejavu-core fonts-texgyre latexmk texlive-xetex \
  texlive-latex-extra texlive-fonts-recommended texlive-lang-greek lmodern git gh curl
if ! command -v google-chrome >/dev/null && ! command -v chromium >/dev/null; then
  tmp_deb=$(mktemp --suffix=.deb)
  curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o "$tmp_deb"
  "${ADMIN[@]}" apt-get install -y "$tmp_deb"
  rm -f "$tmp_deb"
fi
python3 -m venv .venv
.venv/bin/pip install -r .codex/cloud-requirements.txt
mkdir -p .venv/bin
# Environment start instructions put this venv first in PATH.
.venv/bin/python -m unittest discover -s tests -q
.venv/bin/python scripts/validate_html_course.py
printf 'Cloud tools ready. Put %s/.venv/bin first in PATH, then use the repository skill.\n' "$PWD"
