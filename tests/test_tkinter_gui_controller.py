from tts_util.adapters.tkinter_gui_controller import TkinterFloatingController


class FakeSpeechControls:
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


class FakeRoot:
    def __init__(self):
        self.buttons = []
        self.title_text = None
        self.geometry_text = None
        self.resizable_args = None
        self.attributes_calls = []
        self.protocol_calls = []
        self.mainloop_calls = 0
        self.destroy_calls = 0
        self.withdraw_calls = 0
        self.deiconify_calls = 0
        self.lift_calls = 0
        self.after_calls = []

    def title(self, value):
        self.title_text = value

    def geometry(self, value):
        self.geometry_text = value

    def resizable(self, x, y):
        self.resizable_args = (x, y)

    def attributes(self, key, value):
        self.attributes_calls.append((key, value))

    def protocol(self, name, callback):
        self.protocol_calls.append((name, callback))

    def mainloop(self):
        self.mainloop_calls += 1

    def destroy(self):
        self.destroy_calls += 1

    def withdraw(self):
        self.withdraw_calls += 1

    def deiconify(self):
        self.deiconify_calls += 1

    def lift(self):
        self.lift_calls += 1

    def after(self, delay_ms, callback):
        self.after_calls.append(delay_ms)
        callback()


class FakeButton:
    def __init__(self, root, text, command, width):
        self.root = root
        self.text = text
        self.command = command
        self.width = width
        self.grid_calls = []
        root.buttons.append(self)

    def grid(self, **kwargs):
        self.grid_calls.append(kwargs)

    def invoke(self):
        self.command()


class FakeTkModule:
    def __init__(self):
        self.root = FakeRoot()

    def Tk(self):
        return self.root

    def Button(self, root, text, command, width):
        return FakeButton(root, text, command, width)


def test_gui_controller_builds_floating_window_and_buttons():
    controls = FakeSpeechControls()
    fake_tk = FakeTkModule()
    controller = TkinterFloatingController(speech_controls=controls, tk_module=fake_tk)

    controller.run()

    root = fake_tk.root
    assert root.title_text == "TTS Controls"
    assert root.geometry_text == "220x96+40+40"
    assert root.resizable_args == (False, False)
    assert root.attributes_calls == [("-topmost", True)]
    assert root.mainloop_calls == 1
    assert len(root.buttons) == 8
    assert [button.text for button in root.buttons] == [
        "⏮",
        "▶",
        "⏸",
        "⏭",
        "◎",
        "➕",
        "➖",
        "✕",
    ]


def test_gui_controller_buttons_invoke_controls_and_close():
    controls = FakeSpeechControls()
    fake_tk = FakeTkModule()
    controller = TkinterFloatingController(speech_controls=controls, tk_module=fake_tk)

    controller.run()

    root = fake_tk.root
    for button in root.buttons[:-1]:
        button.invoke()

    assert controls.calls == [
        "prev",
        "start",
        "stop",
        "next",
        "current",
        "rate-up",
        "rate-down",
    ]
    assert root.withdraw_calls == 7
    assert root.deiconify_calls == 7
    assert root.lift_calls == 7
    assert root.after_calls == [controller.FOCUS_RETURN_DELAY_MS] * 7

    close_button = root.buttons[-1]
    close_button.invoke()
    assert root.destroy_calls == 1

    wm_delete_callback = root.protocol_calls[0][1]
    wm_delete_callback()
    assert root.destroy_calls == 2


def test_start_button_resumes_after_initial_start():
    controls = FakeSpeechControls()
    fake_tk = FakeTkModule()
    controller = TkinterFloatingController(speech_controls=controls, tk_module=fake_tk)

    controller.run()

    root = fake_tk.root
    start_button = root.buttons[1]
    start_button.invoke()
    start_button.invoke()

    assert controls.calls == ["start", "current"]
