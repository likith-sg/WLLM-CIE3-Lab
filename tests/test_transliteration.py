"""
Unit tests for IndicXlit Transliteration model and service.
"""

import pytest
from models.indicxlit import IndicXlitModel
from services.transliteration_service import TransliterationService


@pytest.fixture
def xlit_service():
    return TransliterationService()


def test_empty_and_whitespace_transliteration(xlit_service):
    """Verifies graceful handling of empty or blank input strings."""
    res = xlit_service.transliterate("")
    assert res["success"] is False
    assert res["error"] == "Empty input text provided."

    res_blank = xlit_service.transliterate("    \n\t  ")
    assert res_blank["success"] is False


def test_simple_word_transliteration(xlit_service):
    """Tests high-frequency greetings and basic words."""
    res = xlit_service.transliterate("namaste")
    assert res["success"] is True
    assert "नमस्ते" in res["devanagari_text"]

    res_shukriya = xlit_service.transliterate("shukriya")
    assert res_shukriya["success"] is True
    assert "शुक्रिया" in res_shukriya["devanagari_text"]


def test_sentence_and_punctuation_preservation(xlit_service):
    """Tests that punctuation marks and whitespace structure are maintained."""
    input_text = "kripya darwaza band kar dijiye."
    res = xlit_service.transliterate(input_text)
    assert res["success"] is True
    assert "कृपया" in res["devanagari_text"]
    assert "दरवाज़ा" in res["devanagari_text"] or "दरवाजा" in res["devanagari_text"]


def test_mixed_hinglish_and_numbers(xlit_service):
    """Tests sentences containing digits and English acronyms."""
    input_text = "meeting room 402 me 10:30 AM par hai!"
    res = xlit_service.transliterate(input_text)
    assert res["success"] is True
    assert "402" in res["devanagari_text"]
    assert "10:30" in res["devanagari_text"]
    assert "!" in res["devanagari_text"]
