#!/bin/bash
set -e

if ! command -v google-chrome >/dev/null; then
  tmpdeb="/tmp/chrome.deb"
  curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o "$tmpdeb"
  sudo apt-get update
  sudo apt-get install -y "$tmpdeb"
  rm -f "$tmpdeb"
fi
