import logging
from typing import Callable, Final, Mapping, Sequence

from pynput import keyboard
from ..core.ports import SpeechControlPort, TriggerControllerPort


logger = logging.getLogger(__name__)


HOTKEY_STOP_SERVICE: Final[str] = ";+q"
HOTKEY_START_SPEAKING: Final[str] = ";+["
HOTKEY_STOP_SPEAKING: Final[str] = ";+]"
HOTKEY_SPEAK_CURRENT: Final[str] = ";+'"
HOTKEY_SPEAK_NEXT: Final[str] = ";+."
HOTKEY_SPEAK_PREV: Final[str] = ";+,"
HOTKEY_RATE_UP: Final[str] = ";+p"
HOTKEY_RATE_DOWN: Final[str] = ";+o"


class PynputHotkeyController(TriggerControllerPort):
    """Binds pynput global hotkeys to high-level speech control actions."""

    def __init__(
        self,
        speech_controls: SpeechControlPort,
        run_hotkeys: Callable[[Mapping[str, Callable[[], None]]], None] | None = None,
        keyboard_module=keyboard,
        key_controller=None,
    ):
        self._speech_controls = speech_controls
        self._keyboard = keyboard_module
        self._key_controller = key_controller or keyboard_module.Controller()
        self._run_hotkeys_handler = run_hotkeys or self._run_hotkeys

    @staticmethod
    def stop() -> None:
        """Stops the service loop by exiting the process."""

        logger.info("Stop requested via hotkey")
        raise SystemExit(0)

    def run(self) -> None:
        """Registers hotkeys and blocks while the global listener is active."""

        hotkey_handlers = {
            HOTKEY_STOP_SERVICE: (self.stop, [HOTKEY_STOP_SERVICE]),
            HOTKEY_START_SPEAKING: (
                self._speech_controls.start_speaking,
                [HOTKEY_START_SPEAKING],
            ),
            HOTKEY_STOP_SPEAKING: (
                self._speech_controls.stop_speaking,
                [HOTKEY_STOP_SPEAKING],
            ),
            HOTKEY_SPEAK_CURRENT: (
                self._speech_controls.speak_current_sentence,
                [HOTKEY_SPEAK_CURRENT, HOTKEY_SPEAK_NEXT, HOTKEY_SPEAK_PREV],
            ),
            HOTKEY_SPEAK_NEXT: (
                self._speech_controls.speak_next_sentence,
                [HOTKEY_SPEAK_CURRENT, HOTKEY_SPEAK_NEXT, HOTKEY_SPEAK_PREV],
            ),
            HOTKEY_SPEAK_PREV: (
                self._speech_controls.speak_prev_sentence,
                [HOTKEY_SPEAK_CURRENT, HOTKEY_SPEAK_NEXT, HOTKEY_SPEAK_PREV],
            ),
            HOTKEY_RATE_UP: (
                self._speech_controls.increment_rate_up,
                [HOTKEY_RATE_UP],
            ),
            HOTKEY_RATE_DOWN: (
                self._speech_controls.increment_rate_down,
                [HOTKEY_RATE_DOWN],
            ),
        }

        hotkeys = {}
        logger.info("Registered hotkeys:")
        for hotkey, (command, clear_hotkeys) in hotkey_handlers.items():
            name = (
                command.__qualname__
                if hasattr(command, "__qualname__")
                else str(command)
            )
            hotkeys[hotkey] = self._clear_and_call(command, clear_hotkeys)
            logger.info("    %s: %s", hotkey, name)

        logger.info("Starting macro service with %s hotkey(s)", len(hotkeys))
        self._run_hotkeys_handler(hotkeys)

    def _clear_and_call(
        self, command: Callable[[], None], hotkeys: Sequence[str]
    ) -> Callable[[], None]:
        def wrapper(*args, **kwargs):
            logger.debug("Clearing %s hotkey(s)", len(hotkeys))
            for hotkey in hotkeys:
                parsed_keys = self._keyboard.HotKey.parse(hotkey)
                for key in parsed_keys:
                    self._key_controller.release(key)
            return command(*args, **kwargs)

        return wrapper

    def _run_hotkeys(self, hotkeys: Mapping[str, Callable[[], None]]) -> None:
        """Default pynput listener loop implementation."""

        with self._keyboard.GlobalHotKeys(hotkeys) as listener:
            listener.join()
