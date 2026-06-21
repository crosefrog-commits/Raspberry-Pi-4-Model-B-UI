#!/usr/bin/env bash
set -euo pipefail

DEVICE="${VOICE_PI_AUDIO_DEVICE:-plughw:1,0}"
OUT="${1:-test_recording.wav}"

echo "=== arecord devices ==="
arecord -l || true

echo
echo "=== recording 5 seconds ==="
echo "device: ${DEVICE}"
arecord -D "${DEVICE}" -f S16_LE -r 16000 -c 1 -d 5 "${OUT}"

echo
echo "saved: ${OUT}"
ls -lh "${OUT}"
echo "playback: aplay ${OUT}"
