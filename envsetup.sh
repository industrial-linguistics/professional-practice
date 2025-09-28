#!/bin/bash
set -e

# Add Revoicer package repository
echo "deb [trusted=yes] https://packages.industrial-linguistics.com/revoicer/debian stable main" | sudo tee /etc/apt/sources.list.d/revoicer.list >/dev/null

# Install base tools
sudo apt-get update
sudo apt-get install -y nodejs npm ffmpeg golang-go jq revoicer

# Install Marp CLI for slide rendering
sudo npm install -g @marp-team/marp-cli

echo "Environment setup complete."
