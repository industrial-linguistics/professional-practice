#!/bin/bash
set -e

# Render slide images from HTML source
python3 scripts/render_html_slides.py --all

# Generate PDFs
GOFLAGS="" go run ./cmd/run_sheets
