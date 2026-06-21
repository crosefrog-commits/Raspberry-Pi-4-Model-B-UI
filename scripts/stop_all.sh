#!/usr/bin/env bash
set -euo pipefail

sudo systemctl stop voice-pi-recorder.service 2>/dev/null || true
pkill -f gunicorn 2>/dev/null || true
pkill -f uvicorn 2>/dev/null || true

echo "Stopped recorder services/processes."
