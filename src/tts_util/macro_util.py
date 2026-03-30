import logging
from .adapters import (
    MultiprocessPyttsx3Speech,
    PynputHotkeyController,
    PynputTextSource,
    TkinterFloatingController,
)
from .core.text_processor import TextProcessor
from .core.speech_controller import SpeechController

logger = logging.getLogger(__name__)


def start(*, use_gui: bool = False):
    """Composes adapters and starts the selected trigger controller loop."""
    speech_controller = SpeechController(
        text_source=PynputTextSource(),
        text_processor=TextProcessor(),
        speech=MultiprocessPyttsx3Speech(),
    )
    controller_cls = TkinterFloatingController if use_gui else PynputHotkeyController
    trigger_controller = controller_cls(speech_controls=speech_controller)
    try:
        trigger_controller.run()
    finally:
        logger.info("Stopping macro service")
        speech_controller.stop_speaking()
