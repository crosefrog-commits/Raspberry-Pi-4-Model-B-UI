import os
import signal
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path

from settings import RECORDINGS_DIR, AUDIO_DEVICE, SAMPLE_RATE, CHANNELS, AUDIO_FORMAT


class Recorder:
    def __init__(self):
        self._lock = threading.Lock()
        self._process = None
        self._current_file = None
        self._started_at = None
        self._last_file = None
        self._last_error = None

    def is_recording(self):
        return self._process is not None and self._process.poll() is None

    def _make_file_path(self):
        date_dir = RECORDINGS_DIR / datetime.now().strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        return date_dir / datetime.now().strftime("%Y-%m-%d_%H%M%S.wav")

    def start(self):
        with self._lock:
            if self.is_recording():
                return {
                    "ok": False,
                    "message": "Already recording.",
                    "recording": True,
                    "file": str(self._current_file) if self._current_file else None,
                }

            self._current_file = self._make_file_path()
            self._started_at = datetime.now(timezone.utc)
            self._last_error = None

            cmd = [
                "arecord",
                "-D", AUDIO_DEVICE,
                "-f", AUDIO_FORMAT,
                "-r", str(SAMPLE_RATE),
                "-c", str(CHANNELS),
                str(self._current_file),
            ]

            try:
                self._process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setsid if hasattr(os, "setsid") else None,
                    text=True,
                )
            except Exception as exc:
                self._last_error = str(exc)
                self._process = None
                self._current_file = None
                self._started_at = None
                return {
                    "ok": False,
                    "message": f"Failed to start recording: {exc}",
                    "recording": False,
                }

            return {
                "ok": True,
                "message": "Recording started.",
                "recording": True,
                "file": str(self._current_file),
            }

    def stop(self):
        with self._lock:
            if not self.is_recording():
                return {
                    "ok": False,
                    "message": "Not recording.",
                    "recording": False,
                    "last_file": str(self._last_file) if self._last_file else None,
                }

            proc = self._process
            saved_file = self._current_file

            try:
                if hasattr(os, "killpg"):
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                else:
                    proc.terminate()

                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if hasattr(os, "killpg"):
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    else:
                        proc.kill()
                    proc.wait(timeout=3)

                if proc.stderr:
                    err = proc.stderr.read()
                    if err:
                        self._last_error = err.strip()[-1200:]

            except Exception as exc:
                self._last_error = str(exc)

            self._process = None
            self._last_file = saved_file
            self._current_file = None
            self._started_at = None

            return {
                "ok": True,
                "message": "Recording stopped.",
                "recording": False,
                "file": str(saved_file) if saved_file else None,
            }

    def status(self):
        with self._lock:
            recording = self.is_recording()
            elapsed = 0
            if recording and self._started_at:
                elapsed = int((datetime.now(timezone.utc) - self._started_at).total_seconds())

            return {
                "recording": recording,
                "file": str(self._current_file) if self._current_file else None,
                "last_file": str(self._last_file) if self._last_file else None,
                "started_at": self._started_at.isoformat() if self._started_at else None,
                "elapsed_seconds": elapsed,
                "audio_device": AUDIO_DEVICE,
                "sample_rate": SAMPLE_RATE,
                "channels": CHANNELS,
                "audio_format": AUDIO_FORMAT,
                "last_error": self._last_error,
            }
