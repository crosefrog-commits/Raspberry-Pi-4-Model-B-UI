#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

sudo cp systemd/voice-pi-recorder.service /etc/systemd/system/voice-pi-recorder.service
sudo systemctl daemon-reload
sudo systemctl enable --now voice-pi-recorder.service

echo "Service installed."
sudo systemctl --no-pager status voice-pi-recorder.service
