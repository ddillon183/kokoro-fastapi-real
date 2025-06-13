"""Text processing pipeline."""

from api.src.services.text_processing.normalizer import normalize_text
from api.src.services.text_processing.phonemizer import phonemize
from api.src.services.text_processing.text_processor import process_text_chunk, smart_split
from api.src.services.text_processing.vocabulary import tokenize


def process_text(text: str) -> list[int]:
    """Process text into token IDs (for backward compatibility)."""
    return process_text_chunk(text)


__all__ = [
    "normalize_text",
    "phonemize",
    "tokenize",
    "process_text",
    "process_text_chunk",
    "smart_split",
]
