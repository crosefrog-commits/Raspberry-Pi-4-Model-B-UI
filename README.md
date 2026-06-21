# Raspberry Pi 4 Model B Voice Touch Recorder UI

Raspberry Pi 4 Model B 기반 음성 녹음 시스템.

GPIO 버튼 또는 Touch UI를 이용하여 음성 녹음을 시작/종료할 수 있으며, 웹 브라우저 기반 사용자 인터페이스를 제공한다.

프로젝트는 Python Backend와 HTML/CSS/JavaScript Frontend로 구성되어 있으며 Raspberry Pi Kiosk Mode 환경에서 동작하도록 설계되었다.

---

## Features

### Audio Recording

* USB Microphone 지원
* WAV 음성 저장
* 녹음 시작/종료 제어
* 파일 자동 생성

### GPIO Integration

* GPIO 버튼 입력 지원
* 물리 버튼을 통한 녹음 제어
* 상태 모니터링

### Web UI

* Touch Screen 최적화
* Fullscreen Kiosk Mode 지원
* 녹음 상태 표시
* 최근 녹음 파일 확인

### System Service

* systemd 서비스 제공
* 부팅 시 자동 실행
* 백그라운드 동작

---

## Hardware Requirements

### Required

* Raspberry Pi 4 Model B
* MicroSD Card (16GB 이상 권장)
* USB Microphone
* Touch Display (선택)
* GPIO Push Button (선택)

### Recommended

* Raspberry Pi OS Bookworm
* Chromium Browser
* Python 3.11+

---

## Software Architecture

```text
Browser UI
    │
    ▼
Frontend
(index.html / app.js)
    │
HTTP
    │
    ▼
Flask Backend
(app.py)
    │
    ├── Recorder Module
    │      └── recorder.py
    │
    └── GPIO Module
           └── gpio_worker.py
    │
    ▼
Audio Files
(recordings/)
```

---

## Project Structure

```text
voice-pi-touch-recorder
│
├── backend/
│   ├── app.py
│   ├── gpio_worker.py
│   ├── recorder.py
│   └── settings.py
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── recordings/
│
├── logs/
│
├── scripts/
│   ├── install.sh
│   ├── run.sh
│   ├── start_kiosk.sh
│   ├── stop_all.sh
│   └── install_service.sh
│
└── systemd/
    └── voice-pi-recorder.service
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/crosefrog-commits/Raspberry-Pi-4-Model-B-UI.git

cd Raspberry-Pi-4-Model-B-UI
```

### Install Dependencies

```bash
chmod +x scripts/install.sh

./scripts/install.sh
```

---

## Run Application

```bash
chmod +x scripts/run.sh

./scripts/run.sh
```

---

## Enable Auto Start

```bash
chmod +x scripts/install_service.sh

./scripts/install_service.sh
```

---

## Logs

로그 저장 위치

```text
logs/
```

실시간 확인

```bash
journalctl -u voice-pi-recorder -f
```

---

## Recordings

녹음 파일 저장 위치

```text
recordings/
```

---

## Kiosk Mode

Touch Screen 환경에서 자동 전체화면 실행

```bash
./scripts/start_kiosk.sh
```

종료

```bash
./scripts/stop_all.sh
```

---

## Development

### Backend

Python

### Frontend

HTML

CSS

JavaScript

### Operating System

Raspberry Pi OS

---

## Future Improvements

* Speech-to-Text Integration
* OpenAI Whisper Support
* Speaker Identification
* Cloud Upload
* AI Voice Analysis
* Dashboard Monitoring
* OTA Update

---

## License

Internal Project

Copyright © XAIKOREA
