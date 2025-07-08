#!/bin/bash
set -e

# Render slide images using Go
GOFLAGS="" go run ./cmd/render-slides

# Generate PDFs
GOFLAGS="" go run ./cmd/run-sheets
