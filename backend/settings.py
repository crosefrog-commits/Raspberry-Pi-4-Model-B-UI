import os
from pathlib import Path

APP_ROOT = Path(os.environ.get("VOICE_PI_ROOT", str(Path.home() / "voice-pi-touch-recorder")))
RECORDINGS_DIR = Path(os.environ.get("VOICE_PI_RECORDINGS_DIR", str(APP_ROOT / "recordings")))
LOG_DIR = Path(os.environ.get("VOICE_PI_LOG_DIR", str(APP_ROOT / "logs")))

AUDIO_DEVICE = os.environ.get("VOICE_PI_AUDIO_DEVICE", "plughw:1,0")
SAMPLE_RATE = int(os.environ.get("VOICE_PI_SAMPLE_RATE", "16000"))
CHANNELS = int(os.environ.get("VOICE_PI_CHANNELS", "1"))
AUDIO_FORMAT = os.environ.get("VOICE_PI_AUDIO_FORMAT", "S16_LE")

ENABLE_GPIO = os.environ.get("VOICE_PI_ENABLE_GPIO", "0") == "1"
START_GPIO = int(os.environ.get("VOICE_PI_START_GPIO", "17"))
STOP_GPIO = int(os.environ.get("VOICE_PI_STOP_GPIO", "27"))

RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
