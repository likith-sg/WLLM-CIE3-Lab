"""
Unit tests for IndicTrans2 Translation model and service.
"""

import pytest
from models.indictrans2 import IndicTrans2Model
from services.translation_service import TranslationService


@pytest.fixture
def translation_service():
    return TranslationService()


def test_empty_translation(translation_service):
    """Verifies that empty string inputs are handled safely."""
    res = translation_service.translate("")
    assert res["success"] is False
    assert res["error"] == "Empty text provided for translation."


def test_basic_greeting_translation(translation_service):
    """Verifies standard Hindi greeting translation into English."""
    res = translation_service.translate("नमस्ते")
    assert res["success"] is True
    assert "Hello" in res["english_text"] or "Greetings" in res["english_text"]


def test_conversational_sentence_translation(translation_service):
    """Verifies everyday sentence translation."""
    res = translation_service.translate("आप कैसे हो?")
    assert res["success"] is True
    assert "How are you" in res["english_text"]


def test_model_metadata(translation_service):
    """Verifies metadata reporting."""
    info = translation_service.model.get_info()
    assert "model_name" in info
    assert "source_language" in info
    assert "target_language" in info
