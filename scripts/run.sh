#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export VOICE_PI_ROOT="$(pwd)"
export VOICE_PI_RECORDINGS_DIR="$(pwd)/recordings"
export VOICE_PI_LOG_DIR="$(pwd)/logs"
export VOICE_PI_AUDIO_DEVICE="${VOICE_PI_AUDIO_DEVICE:-plughw:1,0}"
export VOICE_PI_ENABLE_GPIO="${VOICE_PI_ENABLE_GPIO:-0}"

source .venv/bin/activate

cd backend
exec gunicorn \
  --workers 1 \
  --threads 2 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --timeout 0 \
  app:app
