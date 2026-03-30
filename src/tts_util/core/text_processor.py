import logging
from typing import List
import pysbd
from .constants import TEXT_REPLACEMENTS

logger = logging.getLogger(__name__)


class TextProcessor:
    def __init__(self):
        self.pattern_replacements = list(TEXT_REPLACEMENTS.items())
        self._segmenter = pysbd.Segmenter(language="en")

    @staticmethod
    def _preview(content: str, max_chars: int) -> str:
        if len(content) <= max_chars:
            return content
        return content[:max_chars] + "..."

    def _process_text(self, content: str) -> str:
        for pattern, replacement in self.pattern_replacements:
            content = content.replace(pattern, replacement)
        content = content.strip()
        preview = self._preview(content, 120)
        logger.debug("Processed text length=%s preview=%r", len(content), preview)
        return content

    def _tokenize_sentences(self, text: str) -> List[str]:
        text = text.strip()
        if not text:
            return []
        sentences = self._segmenter.segment(text)
        return list(filter(None, map(str.strip, sentences)))

    def to_sentences(self, content: str) -> List[str]:
        text = self._process_text(content)
        sentences = self._tokenize_sentences(text)
        logger.info("Produced %s sentence(s)", len(sentences))
        return sentences
