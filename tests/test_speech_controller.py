import threading
from tts_util.core.speech_controller import SpeechController


class FakeTextInterface:
    def __init__(self, text="hello"):
        self._text = text

    def retrieve_text(self):
        return self._text


class FakeTextProcessor:
    def __init__(self, sentences=None):
        self._sentences = [] if sentences is None else list(sentences)

    def to_sentences(self, content):
        return list(self._sentences)


class FakeSpeech:
    def __init__(self):
        self.stop_calls = 0
        self.wait_calls = 0
        self.spoken = []

    def stop(self):
        self.stop_calls += 1

    def speak(self, text, rate_added):
        self.spoken.append((text, rate_added))

    def wait_until_done(self):
        self.wait_calls += 1


class BlockingFakeSpeech(FakeSpeech):
    def __init__(self):
        super().__init__()
        self.started = threading.Event()
        self.released = threading.Event()

    def speak(self, text, rate_added):
        self.released.clear()
        super().speak(text, rate_added)
        self.started.set()

    def wait_until_done(self):
        self.wait_calls += 1
        self.released.wait(timeout=1.0)

    def stop(self):
        super().stop()
        self.released.set()


def make_controller(sentences, speech):
    return SpeechController(
        text_source=FakeTextInterface("ignored"),
        text_processor=FakeTextProcessor(sentences),
        speech=speech,
    )


def test_speak_sentence_speaks_feedback_when_empty():
    speech = FakeSpeech()
    macro = make_controller([], speech)
    macro.speak_sentence()
    assert speech.spoken == [("No sentences loaded.", 0)]


def test_speak_sentence_wraps_for_previous():
    speech = FakeSpeech()
    macro = make_controller(["One.", "Two.", "Three."], speech)
    macro.sentences = ["One.", "Two.", "Three."]
    macro.sentence_idx = 0
    macro.speak_sentence(movement=-1)
    assert macro.sentence_idx == 2
    assert speech.spoken[-1] == ("Three.", 0)


def test_finish_mode_speaks_one_sentence_at_a_time_and_updates_index():
    speech = FakeSpeech()
    macro = make_controller(["One.", "Two.", "Three."], speech)
    macro.sentences = ["One.", "Two.", "Three."]
    macro.sentence_idx = 0

    macro.speak_sentence(finish=True)
    macro._join_playback_thread()

    assert [text for text, _ in speech.spoken] == ["One.", "Two.", "Three."]
    assert speech.wait_calls == 3
    assert macro.sentence_idx == 2


def test_stop_keeps_index_on_current_sentence_in_finish_mode():
    speech = BlockingFakeSpeech()
    macro = make_controller(["One.", "Two.", "Three."], speech)
    macro.sentences = ["One.", "Two.", "Three."]
    macro.sentence_idx = 0

    macro.speak_sentence(finish=True)
    assert speech.started.wait(timeout=1.0)

    macro.stop_speaking()

    assert macro.sentence_idx == 0
    assert [text for text, _ in speech.spoken] == ["One."]


def test_increment_rate_speaks_feedback_with_updated_rate():
    speech = FakeSpeech()
    macro = make_controller([], speech)

    macro.increment_rate(15)

    assert macro.rate_added == 15
    assert speech.spoken[-1] == ("Rate added: 15", 15)
