import multiprocessing
import logging
from typing import Optional
from ..core.ports import SpeechPort

logger = logging.getLogger(__name__)


def _speak(text: str, added_rate: int) -> None:
    import pyttsx3

    engine = pyttsx3.init()
    engine.setProperty("rate", engine.getProperty("rate") + added_rate)
    engine.say(text)
    engine.runAndWait()


class MultiprocessPyttsx3Speech(SpeechPort):
    STOP_JOIN_TIMEOUT_SECONDS: float = 1.0

    def __init__(self):
        # Adapter-level process isolates pyttsx3 and allows hard-stop via terminate().
        self._handle: Optional[multiprocessing.Process] = None

    def stop(self) -> None:
        if self._handle is None:
            return
        self._handle.terminate()
        self._handle.join(timeout=self.STOP_JOIN_TIMEOUT_SECONDS)
        if self._handle.is_alive():
            self._handle.kill()
            self._handle.join(timeout=self.STOP_JOIN_TIMEOUT_SECONDS)
        self._handle = None

    def wait_until_done(self) -> None:
        if self._handle is None:
            return
        self._handle.join()
        self._handle = None

    def speak(self, text: str, rate_added: int) -> None:
        self.stop()
        if not text:
            return
        self._handle = multiprocessing.Process(
            target=_speak,
            args=(text, rate_added),
            daemon=True,
        )
        self._handle.start()
