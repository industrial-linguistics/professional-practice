#!/bin/bash
set -e

# Install base tools
sudo apt-get update
sudo apt-get install -y nodejs npm ffmpeg golang-go jq

# Install Marp CLI for slide rendering
sudo npm install -g @marp-team/marp-cli

echo "Environment setup complete."
