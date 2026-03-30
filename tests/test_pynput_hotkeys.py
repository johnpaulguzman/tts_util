from tts_util.adapters.pynput_hotkeys import (
    HOTKEY_RATE_DOWN,
    HOTKEY_RATE_UP,
    HOTKEY_SPEAK_CURRENT,
    HOTKEY_SPEAK_NEXT,
    HOTKEY_SPEAK_PREV,
    HOTKEY_START_SPEAKING,
    HOTKEY_STOP_SERVICE,
    HOTKEY_STOP_SPEAKING,
    PynputHotkeyController,
)


class FakeSpeechController:
    def __init__(self):
        self.calls = []

    def start_speaking(self):
        self.calls.append("start")

    def stop_speaking(self):
        self.calls.append("stop")

    def speak_current_sentence(self):
        self.calls.append("current")

    def speak_next_sentence(self):
        self.calls.append("next")

    def speak_prev_sentence(self):
        self.calls.append("prev")

    def increment_rate_up(self):
        self.calls.append("rate-up")

    def increment_rate_down(self):
        self.calls.append("rate-down")


class FakeHotkeyRunner:
    def __init__(self):
        self.hotkeys = None

    def __call__(self, hotkeys):
        self.hotkeys = hotkeys


class FakeKeyboardController:
    def __init__(self):
        self.released = []

    def release(self, key):
        self.released.append(key)


class FakeKeyboardModule:
    class HotKey:
        @staticmethod
        def parse(hotkey):
            return [f"{hotkey}-first", f"{hotkey}-second"]


class FakeListener:
    def __init__(self, hotkeys):
        self.hotkeys = hotkeys
        self.join_calls = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def join(self):
        self.join_calls += 1


class FakeKeyboardModuleWithListener:
    HotKey = FakeKeyboardModule.HotKey

    def __init__(self):
        self.controllers = []
        self.listeners = []

    def Controller(self):
        controller = FakeKeyboardController()
        self.controllers.append(controller)
        return controller

    def GlobalHotKeys(self, hotkeys):
        listener = FakeListener(hotkeys)
        self.listeners.append(listener)
        return listener


def test_command_controller_registers_all_hotkeys():
    speech_controls = FakeSpeechController()
    runner = FakeHotkeyRunner()
    controller = PynputHotkeyController(
        speech_controls=speech_controls,
        run_hotkeys=runner,
        keyboard_module=FakeKeyboardModule,
        key_controller=FakeKeyboardController(),
    )

    controller.run()

    assert set(runner.hotkeys) == {
        HOTKEY_STOP_SERVICE,
        HOTKEY_START_SPEAKING,
        HOTKEY_STOP_SPEAKING,
        HOTKEY_SPEAK_CURRENT,
        HOTKEY_SPEAK_NEXT,
        HOTKEY_SPEAK_PREV,
        HOTKEY_RATE_UP,
        HOTKEY_RATE_DOWN,
    }


def test_command_controller_clears_related_hotkeys_before_command():
    speech_controls = FakeSpeechController()
    runner = FakeHotkeyRunner()
    keyboard_controller = FakeKeyboardController()
    controller = PynputHotkeyController(
        speech_controls=speech_controls,
        run_hotkeys=runner,
        keyboard_module=FakeKeyboardModule,
        key_controller=keyboard_controller,
    )

    controller.run()

    runner.hotkeys[HOTKEY_SPEAK_CURRENT]()

    assert speech_controls.calls == ["current"]
    assert keyboard_controller.released == [
        f"{HOTKEY_SPEAK_CURRENT}-first",
        f"{HOTKEY_SPEAK_CURRENT}-second",
        f"{HOTKEY_SPEAK_NEXT}-first",
        f"{HOTKEY_SPEAK_NEXT}-second",
        f"{HOTKEY_SPEAK_PREV}-first",
        f"{HOTKEY_SPEAK_PREV}-second",
    ]


def test_command_controller_stop_hotkey_raises_system_exit_and_clears_keys():
    speech_controls = FakeSpeechController()
    runner = FakeHotkeyRunner()
    keyboard_controller = FakeKeyboardController()
    controller = PynputHotkeyController(
        speech_controls=speech_controls,
        run_hotkeys=runner,
        keyboard_module=FakeKeyboardModule,
        key_controller=keyboard_controller,
    )

    controller.run()

    try:
        runner.hotkeys[HOTKEY_STOP_SERVICE]()
        assert False, "Expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 0

    assert keyboard_controller.released == [
        f"{HOTKEY_STOP_SERVICE}-first",
        f"{HOTKEY_STOP_SERVICE}-second",
    ]


def test_command_controller_uses_default_pynput_runner():
    speech_controls = FakeSpeechController()
    keyboard_module = FakeKeyboardModuleWithListener()
    controller = PynputHotkeyController(
        speech_controls=speech_controls,
        keyboard_module=keyboard_module,
    )

    controller.run()

    listener = keyboard_module.listeners[0]
    listener.hotkeys[HOTKEY_RATE_UP]()

    assert listener.join_calls == 1
    assert speech_controls.calls == ["rate-up"]
    assert keyboard_module.controllers[0].released == [
        f"{HOTKEY_RATE_UP}-first",
        f"{HOTKEY_RATE_UP}-second",
    ]
