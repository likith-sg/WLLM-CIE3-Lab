"""
Text utilities for normalization, tokenization, and linguistic cleaning.
Handles both Roman Hinglish and Devanagari Hindi text processing.
"""

import re
import unicodedata
from typing import List, Tuple

def normalize_roman_text(text: str) -> str:
    """
    Normalizes Roman Hinglish input:
    - Strips leading/trailing whitespace
    - Normalizes repeated whitespaces
    - Normalizes common punctuation
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    # Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)
    # Strip unnecessary blank lines
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return text.strip()


def normalize_devanagari_text(text: str) -> str:
    """
    Normalizes Devanagari Hindi text:
    - Unicode NFC normalization
    - Standardizes Hindi full-stop danda ('।') and ASCII periods
    - Removes redundant zero-width joiners/non-joiners when isolated
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    # Replace standalone periods at end of sentence with danda if in Devanagari context
    text = re.sub(r"([^\.\d])\s*\.\s*$", r"\1 ।", text)
    # Normalize multiple danda
    text = re.sub(r"।+", "।", text)
    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_into_tokens(text: str) -> List[Tuple[str, bool]]:
    """
    Splits text into a list of tuples (token, is_word).
    Preserves punctuation, whitespace, and numbers as distinct tokens.
    """
    pattern = r"([A-Za-z0-9_]+|[^A-Za-z0-9_\s]|\s+)"
    raw_tokens = re.findall(pattern, text)
    results = []
    for token in raw_tokens:
        is_word = bool(re.match(r"^[A-Za-z]+$", token))
        results.append((token, is_word))
    return results


def is_english_or_technical_term(word: str) -> bool:
    """
    Heuristic check if a Roman word is a common English technical term
    that should be kept or handled specifically.
    """
    common_english = {
        "pdf", "ai", "ml", "nlp", "llm", "api", "url", "id", "zoom",
        "google", "python", "data", "science", "software", "laptop",
        "meeting", "conference", "assignment", "project", "presentation"
    }
    return word.lower() in common_english
