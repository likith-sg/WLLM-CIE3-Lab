"""
Unit tests for evaluation metrics (CER, Word Accuracy, WER, BLEU, chrF)
and failure analysis categorization.
"""

import pytest
from evaluation.metrics import (
    calculate_cer,
    calculate_word_accuracy,
    calculate_bleu_and_chrf,
    levenshtein_distance
)
from evaluation.error_analysis import diagnose_transliteration_error, ERROR_CATEGORIES


def test_levenshtein_distance_exact_match():
    """Identical sequences must yield distance 0."""
    dist, subs, ins, dels = levenshtein_distance(list("नमस्ते"), list("नमस्ते"))
    assert dist == 0
    assert subs == 0 and ins == 0 and dels == 0


def test_cer_calculation():
    """Tests Character Error Rate with known edit operations."""
    ref = "नमस्ते"
    hyp_identical = "नमस्ते"
    cer_res = calculate_cer(ref, hyp_identical)
    assert cer_res["cer"] == 0.0

    # 1 insertion / substitution
    hyp_mod = "नमस्तेजी"
    cer_mod = calculate_cer(ref, hyp_mod)
    assert cer_mod["cer"] > 0.0


def test_word_accuracy_calculation():
    """Tests Word Accuracy calculation."""
    ref = "मेरा नाम लिखित है"
    hyp = "मेरा नाम लिखित है"
    wa_res = calculate_word_accuracy(ref, hyp)
    assert wa_res["word_accuracy"] == 100.0
    assert wa_res["wer"] == 0.0

    # Partial match
    hyp_partial = "मेरा नाम अमित है"
    wa_partial = calculate_word_accuracy(ref, hyp_partial)
    assert wa_partial["word_accuracy"] == 75.0  # 3 of 4 words match


def test_bleu_and_chrf_scoring():
    """Tests BLEU score computation."""
    ref = "My name is Likith and I live in Bangalore."
    hyp = "My name is Likith and I live in Bangalore."
    scores = calculate_bleu_and_chrf(ref, hyp)
    assert scores["bleu"] == 100.0
    assert scores["chrf"] == 100.0


def test_failure_diagnosis_categories():
    """Tests that diagnoses match recognized taxonomy categories."""
    diag = diagnose_transliteration_error("namaste", "नमस्ते", "नमस्ते")
    assert diag["category"] == "CORRECT"

    diag_matra = diagnose_transliteration_error("hu", "हूँ", "हु")
    assert diag_matra["category_key"] in ERROR_CATEGORIES
