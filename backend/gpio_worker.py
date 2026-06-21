import threading
import time

from settings import ENABLE_GPIO, START_GPIO, STOP_GPIO


class GPIOWorker:
    def __init__(self, recorder):
        self.recorder = recorder
        self.enabled = ENABLE_GPIO
        self.error = None
        self._thread = None

    def start(self):
        if not self.enabled:
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        try:
            from gpiozero import Button

            start_button = Button(START_GPIO, pull_up=True, bounce_time=0.25)
            stop_button = Button(STOP_GPIO, pull_up=True, bounce_time=0.25)

            start_button.when_pressed = lambda: self.recorder.start()
            stop_button.when_pressed = lambda: self.recorder.stop()

            while True:
                time.sleep(1)

        except Exception as exc:
            self.error = str(exc)
            print(f"[GPIO] Disabled: {exc}", flush=True)
