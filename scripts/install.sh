#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

sudo apt update
sudo apt install -y alsa-utils ffmpeg python3-venv python3-pip

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install flask gunicorn gpiozero

mkdir -p recordings logs

echo
echo "Install complete."
echo "Check microphone: arecord -l"
echo "Run app: ./scripts/run.sh"
