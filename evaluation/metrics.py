"""
Quantitative evaluation metrics for Hinglish-to-Hindi transliteration and translation.
Implements:
1. Character Error Rate (CER) using Levenshtein edit distance.
2. Word Accuracy (WA) & Word Error Rate (WER).
3. BLEU score & chrF score for translation quality.
"""

from typing import List, Dict, Any, Tuple
import unicodedata
import re

def levenshtein_distance(seq1: List[Any], seq2: List[Any]) -> Tuple[int, int, int, int]:
    """
    Computes Levenshtein distance between two sequences (characters or words).
    Returns (distance, substitutions, insertions, deletions).
    """
    m, n = len(seq1), len(seq2)
    # dp[i][j] = (dist, subs, ins, dels)
    dp = [[(0, 0, 0, 0) for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = (i, 0, 0, i)  # deletions
    for j in range(1, n + 1):
        dp[0][j] = (j, 0, j, 0)  # insertions

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Substitution
                sub = (dp[i - 1][j - 1][0] + 1, dp[i - 1][j - 1][1] + 1, dp[i - 1][j - 1][2], dp[i - 1][j - 1][3])
                # Deletion (from ref)
                del_op = (dp[i - 1][j][0] + 1, dp[i - 1][j][1], dp[i - 1][j][2], dp[i - 1][j][3] + 1)
                # Insertion (into hyp)
                ins_op = (dp[i][j - 1][0] + 1, dp[i][j - 1][1], dp[i][j - 1][2] + 1, dp[i][j - 1][3])
                
                # Pick minimum distance operation
                min_op = min([sub, del_op, ins_op], key=lambda x: x[0])
                dp[i][j] = min_op

    return dp[m][n]


def normalize_for_eval(text: str) -> str:
    """Normalizes text for consistent metric comparison."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text.strip())
    # Standardize whitespace
    text = re.sub(r"\s+", " ", text)
    return text


def calculate_cer(reference: str, hypothesis: str) -> Dict[str, Any]:
    """
    Calculates Character Error Rate (CER):
    CER = (Substitutions + Insertions + Deletions) / len(reference)
    """
    ref = normalize_for_eval(reference)
    hyp = normalize_for_eval(hypothesis)

    ref_chars = list(ref)
    hyp_chars = list(hyp)

    if not ref_chars:
        return {
            "cer": 0.0 if not hyp_chars else 1.0,
            "distance": len(hyp_chars),
            "substitutions": 0,
            "insertions": len(hyp_chars),
            "deletions": 0,
            "ref_length": 0
        }

    dist, subs, ins, dels = levenshtein_distance(ref_chars, hyp_chars)
    cer_score = dist / len(ref_chars)

    return {
        "cer": round(cer_score, 4),
        "distance": dist,
        "substitutions": subs,
        "insertions": ins,
        "deletions": dels,
        "ref_length": len(ref_chars)
    }


def calculate_word_accuracy(reference: str, hypothesis: str) -> Dict[str, Any]:
    """
    Calculates Word Accuracy and Word Error Rate (WER):
    Word Accuracy = (Correct words) / Total reference words * 100
    WER = (Substitutions + Insertions + Deletions) / Total reference words
    """
    ref = normalize_for_eval(reference)
    hyp = normalize_for_eval(hypothesis)

    ref_words = ref.split()
    hyp_words = hyp.split()

    if not ref_words:
        return {
            "word_accuracy": 100.0 if not hyp_words else 0.0,
            "wer": 0.0 if not hyp_words else 1.0,
            "correct_words": 0,
            "total_ref_words": 0
        }

    dist, subs, ins, dels = levenshtein_distance(ref_words, hyp_words)
    wer_score = dist / len(ref_words)
    
    # Correct words = total reference words minus (substitutions + deletions)
    correct_words = max(0, len(ref_words) - (subs + dels))
    accuracy = (correct_words / len(ref_words)) * 100.0

    return {
        "word_accuracy": round(accuracy, 2),
        "wer": round(wer_score, 4),
        "correct_words": correct_words,
        "substitutions": subs,
        "insertions": ins,
        "deletions": dels,
        "total_ref_words": len(ref_words)
    }


def calculate_bleu_and_chrf(reference: str, hypothesis: str) -> Dict[str, float]:
    """
    Calculates BLEU score and chrF (Character n-gram F-score) for translation quality.
    Uses sacrebleu if available, with a standard fallback.
    """
    ref = normalize_for_eval(reference)
    hyp = normalize_for_eval(hypothesis)

    if not ref or not hyp:
        return {"bleu": 0.0, "chrf": 0.0}

    try:
        import sacrebleu
        bleu = sacrebleu.sentence_bleu(hyp, [ref]).score
        chrf = sacrebleu.sentence_chrf(hyp, [ref]).score
        return {"bleu": round(bleu, 2), "chrf": round(chrf, 2)}
    except Exception:
        # Simple n-gram BLEU approximation fallback
        ref_words = ref.lower().split()
        hyp_words = hyp.lower().split()
        matches = sum(1 for w in hyp_words if w in ref_words)
        precision = matches / len(hyp_words) if hyp_words else 0.0
        recall = matches / len(ref_words) if ref_words else 0.0
        f1 = (2 * precision * recall / (precision + recall)) * 100 if (precision + recall) > 0 else 0.0
        return {"bleu": round(f1, 2), "chrf": round(f1, 2)}
