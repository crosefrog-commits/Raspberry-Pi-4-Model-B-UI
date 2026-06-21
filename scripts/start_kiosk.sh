#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:8000}"

if command -v chromium >/dev/null 2>&1; then
  BROWSER="chromium"
elif command -v chromium-browser >/dev/null 2>&1; then
  BROWSER="chromium-browser"
else
  echo "Chromium is not installed."
  echo "Install: sudo apt install -y chromium"
  exit 1
fi

exec "$BROWSER" \
  --kiosk "$URL" \
  --window-size=480,320 \
  --force-device-scale-factor=0.75 \
  --hide-scrollbars \
  --overscroll-history-navigation=0 \
  --lang=en-US \
  --disable-translate \
  --disable-features=Translate,TranslateUI \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --autoplay-policy=no-user-gesture-required \
  --user-data-dir=/tmp/voice-pi-chromium-profile
