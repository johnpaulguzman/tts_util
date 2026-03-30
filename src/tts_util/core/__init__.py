from .ports import (
    SpeechControlPort,
    SpeechPort,
    TextSourcePort,
    TriggerControllerPort,
)
from .text_processor import TextProcessor
from tts_util.core.speech_controller import SpeechController

TextInterface = TextProcessor

__all__ = [
    "TriggerControllerPort",
    "SpeechControlPort",
    "SpeechPort",
    "TextSourcePort",
    "TextProcessor",
    "TextInterface",
    "SpeechController",
]
