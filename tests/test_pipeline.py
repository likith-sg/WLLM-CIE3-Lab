"""
Integration tests for the full multi-stage pipeline:
Roman Hinglish -> IndicXlit -> BharatGen Param-1 -> IndicTrans2.
"""

import pytest
from services.pipeline_service import PipelineService


@pytest.fixture
def pipeline():
    return PipelineService()


def test_full_pipeline_end_to_end(pipeline):
    """
    Tests end-to-end execution on the primary project specification sentence:
    'mera naam likith hai aur mai bangalore me rehta hu'
    """
    input_text = "mera naam likith hai aur mai bangalore me rehta hu"
    res = pipeline.process_all(input_text, apply_enhancement=True)

    assert res["success"] is True
    assert res["original_input"] == input_text
    # Check transliterated output contains expected keywords
    assert "नाम" in res["transliterated_hindi"]
    assert "लिखित" in res["transliterated_hindi"]
    assert "बैंगलोर" in res["transliterated_hindi"]
    # Check writing enhancement normalized punctuation or nasalization
    assert len(res["improved_hindi"]) > 0
    # Check English translation produced
    assert "Likith" in res["english_translation"] or "Bangalore" in res["english_translation"]
    assert res["total_latency_ms"] > 0


def test_pipeline_individual_stages(pipeline):
    """Verifies that individual services can be called independently."""
    # Stage 1: Transliterate
    xlit_res = pipeline.xlit.transliterate("dhanyawad")
    assert xlit_res["success"] is True
    assert "धन्यवाद" in xlit_res["devanagari_text"]

    # Stage 2: Improve
    improve_res = pipeline.writing.improve_writing("धन्यवाद")
    assert improve_res["success"] is True

    # Stage 3: Translate
    trans_res = pipeline.translation.translate("धन्यवाद")
    assert trans_res["success"] is True
    assert "Thank you" in trans_res["english_text"]
