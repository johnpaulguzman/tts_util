import types

from tts_util.adapters import pyttsx3_speech
from tts_util.adapters.pyttsx3_speech import MultiprocessPyttsx3Speech, _speak


class FakeProcess:
    def __init__(self, target=None, args=(), daemon=False):
        self.target = target
        self.args = args
        self.daemon = daemon
        self.started = False
        self.alive = False
        self.terminated = False
        self.killed = False
        self.join_calls = []

    def start(self):
        self.started = True
        self.alive = True

    def is_alive(self):
        return self.alive

    def terminate(self):
        self.terminated = True
        self.alive = False

    def kill(self):
        self.killed = True
        self.alive = False

    def join(self, timeout=None):
        self.join_calls.append(timeout)
        self.alive = False


class FakeEngine:
    def __init__(self):
        self.rate = 120
        self.set_calls = []
        self.say_calls = []
        self.run_calls = 0

    def getProperty(self, key):
        assert key == "rate"
        return self.rate

    def setProperty(self, key, value):
        self.set_calls.append((key, value))
        if key == "rate":
            self.rate = value

    def say(self, text):
        self.say_calls.append(text)

    def runAndWait(self):
        self.run_calls += 1


def test_stop_noop_when_no_active_process():
    adapter = MultiprocessPyttsx3Speech()

    adapter.stop()

    assert adapter._handle is None


def test_stop_terminates_alive_process_and_clears_handle():
    adapter = MultiprocessPyttsx3Speech()
    proc = FakeProcess()
    proc.alive = True
    adapter._handle = proc

    adapter.stop()

    assert proc.terminated is True
    assert proc.join_calls == [adapter.STOP_JOIN_TIMEOUT_SECONDS]
    assert adapter._handle is None


def test_wait_until_done_joins_and_clears_handle():
    adapter = MultiprocessPyttsx3Speech()
    proc = FakeProcess()
    adapter._handle = proc

    adapter.wait_until_done()

    assert proc.join_calls == [None]
    assert adapter._handle is None


def test_speak_starts_new_process_for_non_empty_text(monkeypatch):
    created = []

    def fake_process_ctor(*, target, args, daemon):
        proc = FakeProcess(target=target, args=args, daemon=daemon)
        created.append(proc)
        return proc

    monkeypatch.setattr(pyttsx3_speech.multiprocessing, "Process", fake_process_ctor)

    adapter = MultiprocessPyttsx3Speech()
    adapter.speak("hello", 15)

    assert len(created) == 1
    assert created[0].target is _speak
    assert created[0].args == ("hello", 15)
    assert created[0].daemon is True
    assert created[0].started is True
    assert adapter._handle is created[0]


def test_speak_empty_text_stops_existing_process_without_starting_new(monkeypatch):
    created = []

    def fake_process_ctor(*, target, args, daemon):
        proc = FakeProcess(target=target, args=args, daemon=daemon)
        created.append(proc)
        return proc

    monkeypatch.setattr(pyttsx3_speech.multiprocessing, "Process", fake_process_ctor)

    adapter = MultiprocessPyttsx3Speech()
    existing = FakeProcess()
    existing.alive = True
    adapter._handle = existing

    adapter.speak("", 10)

    assert created == []
    assert existing.terminated is True
    assert adapter._handle is None


def test_stop_escalates_to_kill_when_process_survives_terminate():
    class StubbornProcess(FakeProcess):
        def terminate(self):
            self.terminated = True

        def join(self, timeout=None):
            self.join_calls.append(timeout)

        def kill(self):
            self.killed = True
            self.alive = False

    adapter = MultiprocessPyttsx3Speech()
    proc = StubbornProcess()
    proc.alive = True
    adapter._handle = proc

    adapter.stop()

    assert proc.terminated is True
    assert proc.killed is True
    assert proc.join_calls == [
        adapter.STOP_JOIN_TIMEOUT_SECONDS,
        adapter.STOP_JOIN_TIMEOUT_SECONDS,
    ]
    assert adapter._handle is None


def test_stop_force_kills_process_when_terminate_fails():
    class UnstoppableProcess(FakeProcess):
        def terminate(self):
            self.terminated = True

        def join(self, timeout=None):
            self.join_calls.append(timeout)

        def kill(self):
            self.killed = True

    adapter = MultiprocessPyttsx3Speech()
    proc = UnstoppableProcess()
    proc.alive = True
    adapter._handle = proc

    adapter.stop()

    assert proc.terminated is True
    assert proc.killed is True
    assert adapter._handle is None


def test__speak_applies_rate_offset_and_runs_engine(monkeypatch):
    engine = FakeEngine()
    fake_pyttsx3 = types.SimpleNamespace(init=lambda: engine)
    monkeypatch.setitem(__import__("sys").modules, "pyttsx3", fake_pyttsx3)

    _speak("sample text", 20)

    assert engine.set_calls == [("rate", 140)]
    assert engine.say_calls == ["sample text"]
    assert engine.run_calls == 1
