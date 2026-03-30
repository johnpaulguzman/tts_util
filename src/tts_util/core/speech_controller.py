import logging
import threading
from typing import List
from .ports import SpeechPort, TextSourcePort
from .text_processor import TextProcessor

logger = logging.getLogger(__name__)


class SpeechController:
    RATE_STEP = 15
    THREAD_JOIN_TIMEOUT_SECONDS = 1.0

    @staticmethod
    def _preview(content: str, max_chars: int = 60) -> str:
        if len(content) <= max_chars:
            return content
        return content[:max_chars] + "..."

    def __init__(
        self,
        *,
        text_source: TextSourcePort,
        text_processor: TextProcessor,
        speech: SpeechPort,
    ):
        self.rate_added = 0
        self.sentences: List[str] = []
        self.sentence_idx = 0
        # Controller-level thread runs sentence sequencing so hotkeys remain responsive.
        self._stop_event = threading.Event()
        self._playback_thread: threading.Thread | None = None
        self._text_source = text_source
        self._text_processor = text_processor
        self._speech = speech

    def _join_playback_thread(self):
        thread = self._playback_thread
        if thread is None:
            return
        if thread is threading.current_thread():
            return
        thread.join(timeout=self.THREAD_JOIN_TIMEOUT_SECONDS)
        if not thread.is_alive():
            self._playback_thread = None

    def _play_sequence_from_index(self, start_idx: int):
        for idx in range(start_idx, len(self.sentences)):
            if self._stop_event.is_set():
                break
            self.sentence_idx = idx
            text = self.sentences[idx]
            preview = self._preview(text)
            logger.info(
                "Speaking sentence %s/%s preview=%r",
                idx + 1,
                len(self.sentences),
                preview,
            )
            try:
                self._speech.speak(text, self.rate_added)
                self._speech.wait_until_done()
            except Exception:
                logger.exception("Failed while speaking sentence index=%s", idx)
                break
            if self._stop_event.is_set():
                break
        self._playback_thread = None

    def stop_speaking(self):
        logger.debug("Stopping active speech")
        self._stop_event.set()
        try:
            self._speech.stop()
        except Exception:
            logger.exception("Failed to stop speech")
        self._join_playback_thread()

    def _speak(self, text: str):
        if not text:
            logger.debug("Skipping speak for empty text")
            return
        preview = self._preview(text)
        logger.info("Speaking text (len=%s) preview=%r", len(text), preview)
        try:
            self._speech.speak(text, self.rate_added)
        except Exception:
            logger.exception("Failed to speak text")

    def increment_rate(self, amount: int):
        self.stop_speaking()
        self.rate_added += amount
        self._stop_event.clear()
        feedback = f"Rate added: {round(self.rate_added)}"
        logger.info("Adjusted speech rate offset to %s", self.rate_added)
        self._speak(feedback)

    def start_speaking(self):
        logger.info("Loading selected text and starting speech")
        raw_text = self._text_source.retrieve_text()
        self.sentences = self._text_processor.to_sentences(raw_text)
        self.sentence_idx = 0
        logger.info("Loaded %s sentence(s)", len(self.sentences))
        self.speak_sentence(finish=True)

    def speak_sentence(self, movement: int = 0, finish: bool = False):
        logger.debug("Speak sentence movement=%s finish=%s", movement, finish)
        if not self.sentences:
            feedback = "No sentences loaded."
            logger.info("No sentences loaded")
            self._speak(feedback)
            return

        self.stop_speaking()
        self._stop_event.clear()
        self.sentence_idx = (self.sentence_idx + movement) % len(self.sentences)
        logger.debug("Sentence index=%s of %s", self.sentence_idx, len(self.sentences))
        if not finish:
            text = self.sentences[self.sentence_idx]
            self._speak(text)
            return

        # Background sequencing thread delegates each sentence to the speech adapter.
        self._playback_thread = threading.Thread(
            target=self._play_sequence_from_index,
            args=(self.sentence_idx,),
            daemon=True,
        )
        self._playback_thread.start()

    def speak_current_sentence(self):
        self.speak_sentence(0, finish=True)

    def speak_next_sentence(self):
        self.speak_sentence(1)

    def speak_prev_sentence(self):
        self.speak_sentence(-1)

    def increment_rate_up(self):
        self.increment_rate(self.RATE_STEP)

    def increment_rate_down(self):
        self.increment_rate(-self.RATE_STEP)
