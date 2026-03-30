from ..core.ports import TextSourcePort
import sys
import time
from pynput import keyboard, mouse
import pyperclip


class PynputTextSource(TextSourcePort):
    COPY_WAIT = 0.10
    MACOS_PLATFORM = "darwin"
    MACOS_COPY_HOTKEY = "<cmd>+c"
    DEFAULT_COPY_HOTKEY = "<ctrl>+c"

    @staticmethod
    def clipboard_getter() -> str:
        return pyperclip.paste()

    @staticmethod
    def platform_getter() -> str:
        return sys.platform

    def __init__(self):
        self._keyboard = keyboard
        self._mouse = mouse
        self._keyboard_controller = keyboard.Controller()
        self._mouse_controller = mouse.Controller()

    def _input_hotkey(self, hotkey: str) -> None:
        parsed_hotkey = self._keyboard.HotKey.parse(hotkey)
        for key in parsed_hotkey:
            self._keyboard_controller.press(key)
        for key in reversed(parsed_hotkey):
            self._keyboard_controller.release(key)

    @classmethod
    def copy_hotkey(cls) -> str:
        if cls.platform_getter() == cls.MACOS_PLATFORM:
            return cls.MACOS_COPY_HOTKEY
        return cls.DEFAULT_COPY_HOTKEY

    def retrieve_text(self) -> str:
        self._input_hotkey(self.copy_hotkey())
        time.sleep(self.COPY_WAIT)
        copied = self.clipboard_getter()
        self._mouse_controller.click(self._mouse.Button.left)  # Clear current selection
        return copied
