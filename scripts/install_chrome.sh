#!/bin/bash
set -e

if ! command -v google-chrome >/dev/null; then
  curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb
  sudo apt-get update
  sudo apt-get install -y /tmp/chrome.deb
fi
