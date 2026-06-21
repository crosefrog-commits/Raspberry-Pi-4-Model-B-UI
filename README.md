# Voice Pi Recorder Stable EN

Stable Raspberry Pi 4 voice recorder for small GPIO touch LCDs.

## Design

- UI language: English only
- Browser translation: disabled by HTML metadata and Chromium kiosk flags
- Backend: Flask + Gunicorn
- Audio: ALSA `arecord`
- Frontend: static HTML/CSS/JavaScript
- Runtime: no React, no Node.js, no Electron, no Docker
- Target: Raspberry Pi 4 with 2GB RAM and 3.5 inch SPI touch LCD

## Install

```bash
cd ~/voice-pi-touch-recorder
chmod +x scripts/*.sh
./scripts/install.sh
```

## Run

```bash
./scripts/run.sh
```

Open:

```text
http://localhost:8000
http://<raspberry-pi-ip>:8000
```

## Kiosk

```bash
./scripts/start_kiosk.sh
```

## Audio check

```bash
arecord -l
./scripts/check_audio.sh
```

If your mic is not `plughw:1,0`, run:

```bash
VOICE_PI_AUDIO_DEVICE=plughw:2,0 ./scripts/run.sh
```

## Systemd

```bash
./scripts/install_service.sh
sudo systemctl status voice-pi-recorder.service
```


## Micro UI

This version removes all footer/status details except state and timer.

Kiosk default scale is set to 0.75.

If the screen is still cropped:

```bash
cd ~/voice-pi-touch-recorder
DISPLAY=:0 ./scripts/start_kiosk_scale.sh 0.65
```

Try scale values:

```text
0.75
0.70
0.65
0.60
```
