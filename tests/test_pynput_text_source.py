import tts_util.adapters.pynput_text_source as text_source_module
from tts_util.adapters.pynput_text_source import PynputTextSource


def test_copy_hotkey_uses_command_on_macos(monkeypatch):
    monkeypatch.setattr(PynputTextSource, "platform_getter", staticmethod(lambda: "darwin"))

    assert PynputTextSource.copy_hotkey() == "<cmd>+c"


def test_copy_hotkey_uses_control_on_windows(monkeypatch):
    monkeypatch.setattr(PynputTextSource, "platform_getter", staticmethod(lambda: "win32"))

    assert PynputTextSource.copy_hotkey() == "<ctrl>+c"


def test_retrieve_text_uses_platform_copy_hotkey(monkeypatch):
    calls = []
    sleeps = []
    clicks = []

    class FakeMouseButton:
        left = "left"

    class FakeMouseController:
        def click(self, button, count=1):
            clicks.append((button, count))

    source = PynputTextSource.__new__(PynputTextSource)
    source._input_hotkey = calls.append
    source._mouse = type("FakeMouse", (), {"Button": FakeMouseButton})
    source._mouse_controller = FakeMouseController()
    monkeypatch.setattr(PynputTextSource, "platform_getter", staticmethod(lambda: "darwin"))
    monkeypatch.setattr(PynputTextSource, "clipboard_getter", staticmethod(lambda: "selected text"))
    monkeypatch.setattr(text_source_module.time, "sleep", sleeps.append)

    assert source.retrieve_text() == "selected text"
    assert calls == ["<cmd>+c"]
    assert sleeps == [PynputTextSource.COPY_WAIT]
    assert clicks == [("left", 1)]


def test_input_hotkey_releases_keys_in_reverse_order():
    class FakeController:
        def __init__(self):
            self.pressed = []
            self.released = []

        def press(self, key):
            self.pressed.append(key)

        def release(self, key):
            self.released.append(key)

    class FakeKeyboard:
        class HotKey:
            @staticmethod
            def parse(_hotkey):
                return ["ctrl", "shift", "c"]

    source = PynputTextSource.__new__(PynputTextSource)
    source._keyboard = FakeKeyboard
    source._keyboard_controller = FakeController()

    source._input_hotkey("<ctrl>+<shift>+c")

    assert source._keyboard_controller.pressed == ["ctrl", "shift", "c"]
    assert source._keyboard_controller.released == ["c", "shift", "ctrl"]
