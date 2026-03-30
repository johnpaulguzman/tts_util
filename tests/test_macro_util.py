import pytest
import tts_util.macro_util as macro_util


class FakeCommandController:
    def __init__(self, error=None):
        self.error = error
        self.run_calls = 0

    @staticmethod
    def stop():
        raise AssertionError(
            "stop should not be called during macro_util composition tests"
        )

    def run(self):
        self.run_calls += 1
        if self.error is not None:
            raise self.error


class FakeMacro:
    def __init__(self):
        self.hotkeys = {";+[": lambda: None}
        self.stop_calls = 0

    def stop_speaking(self):
        self.stop_calls += 1

    def start_speaking(self):
        pass

    def speak_sentence(self, movement=0, finish=False):
        pass

    def increment_rate(self, amount):
        pass

    def speak_current_sentence(self):
        pass

    def speak_next_sentence(self):
        pass

    def speak_prev_sentence(self):
        pass

    def increment_rate_up(self):
        pass

    def increment_rate_down(self):
        pass


def test_macro_start_cleans_up_speech_on_controller_error(monkeypatch):
    fake_speech_controller = FakeMacro()
    fake_trigger_controller = FakeCommandController(error=RuntimeError("boom"))
    captured = {}

    def controller_factory(**kwargs):
        captured.update(kwargs)
        return fake_trigger_controller

    monkeypatch.setattr(macro_util, "TextProcessor", lambda: object())
    monkeypatch.setattr(macro_util, "PynputTextSource", lambda: object())
    monkeypatch.setattr(macro_util, "MultiprocessPyttsx3Speech", lambda: object())
    monkeypatch.setattr(
        macro_util, "SpeechController", lambda **kwargs: fake_speech_controller
    )
    monkeypatch.setattr(macro_util, "PynputHotkeyController", controller_factory)
    with pytest.raises(RuntimeError, match="boom"):
        macro_util.start()
    assert captured["speech_controls"] is fake_speech_controller
    assert fake_trigger_controller.run_calls == 1
    assert fake_speech_controller.stop_calls == 1


def test_macro_start_runs_command_controller(monkeypatch):
    fake_speech_controller = FakeMacro()
    fake_trigger_controller = FakeCommandController()
    captured = {}

    def controller_factory(**kwargs):
        captured.update(kwargs)
        return fake_trigger_controller

    monkeypatch.setattr(macro_util, "TextProcessor", lambda: object())
    monkeypatch.setattr(macro_util, "PynputTextSource", lambda: object())
    monkeypatch.setattr(macro_util, "MultiprocessPyttsx3Speech", lambda: object())
    monkeypatch.setattr(
        macro_util, "SpeechController", lambda **kwargs: fake_speech_controller
    )
    monkeypatch.setattr(macro_util, "PynputHotkeyController", controller_factory)
    macro_util.start()
    assert captured["speech_controls"] is fake_speech_controller
    assert fake_trigger_controller.run_calls == 1
    assert fake_speech_controller.stop_calls == 1


def test_macro_start_with_gui_uses_tkinter_controller(monkeypatch):
    fake_speech_controller = FakeMacro()
    fake_trigger_controller = FakeCommandController()
    captured = {}

    def controller_factory(**kwargs):
        captured.update(kwargs)
        return fake_trigger_controller

    monkeypatch.setattr(macro_util, "TextProcessor", lambda: object())
    monkeypatch.setattr(macro_util, "PynputTextSource", lambda: object())
    monkeypatch.setattr(macro_util, "MultiprocessPyttsx3Speech", lambda: object())
    monkeypatch.setattr(
        macro_util, "SpeechController", lambda **kwargs: fake_speech_controller
    )
    monkeypatch.setattr(macro_util, "TkinterFloatingController", controller_factory)

    macro_util.start(use_gui=True)

    assert captured["speech_controls"] is fake_speech_controller
    assert fake_trigger_controller.run_calls == 1
    assert fake_speech_controller.stop_calls == 1
