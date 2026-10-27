#!/usr/bin/env bash
# Install the image producer's Linux tools without audio-provider credentials.
set -euo pipefail
cd "$(dirname "$0")/.."
ADMIN=()
CAN_INSTALL=0
if [[ $(id -u) -eq 0 ]]; then
  CAN_INSTALL=1
elif command -v sudo >/dev/null && sudo -n true 2>/dev/null; then
  ADMIN=(sudo -n)
  CAN_INSTALL=1
fi
if [[ $CAN_INSTALL -eq 1 ]]; then
  "${ADMIN[@]}" apt-get update
  "${ADMIN[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip sqlite3 graphviz nodejs npm \
    ffmpeg poppler-utils fonts-dejavu-core fonts-texgyre latexmk texlive-xetex \
    texlive-latex-extra texlive-fonts-recommended texlive-lang-greek lmodern git gh curl
else
  # Managed Cloud supplies these in its base image; it does not grant sudo.
  missing=()
  for executable in python3 sqlite3 dot node npm ffmpeg pdftotext xelatex latexmk git gh curl; do
    command -v "$executable" >/dev/null || missing+=("$executable")
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    printf 'Provision missing tools in the environment install script: %s\n' "${missing[*]}" >&2
    exit 1
  fi
fi
if ! command -v google-chrome >/dev/null && ! command -v chromium >/dev/null; then
  if [[ $CAN_INSTALL -ne 1 ]]; then
    printf 'Provision Chrome/Chromium in the environment install script.\n' >&2
    exit 1
  fi
  tmp_deb=$(mktemp --suffix=.deb)
  curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o "$tmp_deb"
  "${ADMIN[@]}" apt-get install -y "$tmp_deb"
  rm -f "$tmp_deb"
fi
if command -v uv >/dev/null; then
  uv venv --python "$(command -v python3)" .venv
  uv pip install --python .venv/bin/python -r .codex/cloud-requirements.txt
else
  python3 -m venv .venv
  .venv/bin/pip install -r .codex/cloud-requirements.txt
fi
mkdir -p .venv/bin
# Environment start instructions put this venv first in PATH.
.venv/bin/python -m unittest discover -s tests -q
.venv/bin/python scripts/validate_html_course.py
printf 'Cloud tools ready. Put %s/.venv/bin first in PATH, then use the repository skill.\n' "$PWD"
