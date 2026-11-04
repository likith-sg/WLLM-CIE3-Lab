"""
Automated Evaluation Runner for Hinglish Smart Writing Assistant.
Executes quantitative evaluation across all 40 Aksharantar & curated test cases.
Calculates CER, Word Accuracy, WER, BLEU, chrF, and error distributions.
"""

import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json
import logging
from typing import Dict, Any, List

from evaluation.metrics import (
    calculate_cer,
    calculate_word_accuracy,
    calculate_bleu_and_chrf,
    normalize_for_eval
)
from evaluation.error_analysis import (
    diagnose_transliteration_error,
    generate_failure_analysis_report
)
from services.pipeline_service import PipelineService

logger = logging.getLogger(__name__)

DATASET_FILE = Path(__file__).resolve().parent / "test_dataset.json"
RESULTS_FILE = Path(__file__).resolve().parent / "evaluation_results.json"


def run_full_evaluation(pipeline: PipelineService = None) -> Dict[str, Any]:
    """
    Executes benchmark evaluation on the test dataset.
    Returns aggregated metrics and detailed per-sample records.
    """
    if pipeline is None:
        pipeline = PipelineService()

    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    total_cases = len(dataset)
    processed_records = []
    
    total_cer_sum = 0.0
    total_wer_sum = 0.0
    total_word_acc_sum = 0.0
    total_bleu_sum = 0.0
    total_chrf_sum = 0.0

    total_ref_chars = 0
    total_char_dist = 0

    category_stats: Dict[str, Dict[str, Any]] = {}

    for item in dataset:
        cat = item["category"]
        if cat not in category_stats:
            category_stats[cat] = {
                "count": 0,
                "cer_sum": 0.0,
                "acc_sum": 0.0,
                "bleu_sum": 0.0,
                "perfect_matches": 0
            }

        # 1. Real pipeline inference
        result = pipeline.process_all(item["input_hinglish"], apply_enhancement=True)
        pred_hindi = result["transliterated_hindi"]
        pred_english = result["english_translation"]

        # 2. Metric computations
        cer_metrics = calculate_cer(item["reference_hindi"], pred_hindi)
        wa_metrics = calculate_word_accuracy(item["reference_hindi"], pred_hindi)
        trans_metrics = calculate_bleu_and_chrf(item["reference_english"], pred_english)

        cer = cer_metrics["cer"]
        wa = wa_metrics["word_accuracy"]
        wer = wa_metrics["wer"]
        bleu = trans_metrics["bleu"]
        chrf = trans_metrics["chrf"]

        # Update running aggregates
        total_cer_sum += cer
        total_wer_sum += wer
        total_word_acc_sum += wa
        total_bleu_sum += bleu
        total_chrf_sum += chrf

        total_ref_chars += cer_metrics["ref_length"]
        total_char_dist += cer_metrics["distance"]

        # Update category aggregates
        category_stats[cat]["count"] += 1
        category_stats[cat]["cer_sum"] += cer
        category_stats[cat]["acc_sum"] += wa
        category_stats[cat]["bleu_sum"] += bleu
        if normalize_for_eval(item["reference_hindi"]) == normalize_for_eval(pred_hindi):
            category_stats[cat]["perfect_matches"] += 1

        # Failure diagnosis
        diag = diagnose_transliteration_error(
            item["input_hinglish"],
            item["reference_hindi"],
            pred_hindi
        )

        record = {
            "id": item["id"],
            "category": cat,
            "input_hinglish": item["input_hinglish"],
            "reference_hindi": item["reference_hindi"],
            "predicted_hindi": pred_hindi,
            "improved_hindi": result.get("improved_hindi", pred_hindi),
            "reference_english": item["reference_english"],
            "predicted_english": pred_english,
            "cer": cer,
            "word_accuracy": wa,
            "wer": wer,
            "bleu": bleu,
            "chrf": chrf,
            "diagnosis": diag,
            "status": "evaluated"
        }
        processed_records.append(record)

    # Calculate overall averages
    avg_cer = round(total_cer_sum / total_cases, 4) if total_cases else 0.0
    corpus_cer = round(total_char_dist / total_ref_chars, 4) if total_ref_chars else 0.0
    avg_word_acc = round(total_word_acc_sum / total_cases, 2) if total_cases else 0.0
    avg_wer = round(total_wer_sum / total_cases, 4) if total_cases else 0.0
    avg_bleu = round(total_bleu_sum / total_cases, 2) if total_cases else 0.0
    avg_chrf = round(total_chrf_sum / total_cases, 2) if total_cases else 0.0

    # Format category breakdown
    category_summary = []
    for cat_name, stats in category_stats.items():
        cnt = stats["count"]
        category_summary.append({
            "category": cat_name,
            "test_cases": cnt,
            "avg_cer": round(stats["cer_sum"] / cnt, 4) if cnt else 0.0,
            "avg_word_accuracy": round(stats["acc_sum"] / cnt, 2) if cnt else 0.0,
            "avg_bleu": round(stats["bleu_sum"] / cnt, 2) if cnt else 0.0,
            "perfect_matches": stats["perfect_matches"],
            "accuracy_rate": round((stats["perfect_matches"] / cnt) * 100, 1) if cnt else 0.0
        })

    # Error analysis report
    failure_report = generate_failure_analysis_report(processed_records)

    summary = {
        "total_test_cases": total_cases,
        "average_cer": avg_cer,
        "corpus_cer": corpus_cer,
        "average_word_accuracy": avg_word_acc,
        "average_wer": avg_wer,
        "average_bleu": avg_bleu,
        "average_chrf": avg_chrf,
        "category_breakdown": category_summary,
        "failure_analysis": failure_report,
        "detailed_results": processed_records
    }

    # Persist results
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return summary


if __name__ == "__main__":
    print("Executing quantitative evaluation across all 40 test cases...")
    res = run_full_evaluation()
    print("=" * 60)
    print("Hinglish Smart Writing Assistant - Evaluation Summary")
    print("=" * 60)
    print(f"Total Test Cases:       {res['total_test_cases']}")
    print(f"Average CER:            {res['average_cer'] * 100:.2f}%")
    print(f"Corpus-Level CER:       {res['corpus_cer'] * 100:.2f}%")
    print(f"Average Word Accuracy:  {res['average_word_accuracy']:.2f}%")
    print(f"Average BLEU Score:     {res['average_bleu']:.2f}")
    print(f"Average chrF Score:     {res['average_chrf']:.2f}")
    print(f"Categorized Failures:   {res['failure_analysis']['total_failures']}")
    print("=" * 60)
