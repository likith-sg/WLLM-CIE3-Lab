"""
Error analysis and failure taxonomy module for Hinglish-to-Hindi transliteration,
writing enhancement, and translation.
Categorizes system errors according to CS3235 evaluation criteria.
"""

from typing import List, Dict, Any

ERROR_CATEGORIES = {
    "AMBIGUOUS_SPELLING": {
        "name": "Ambiguous Roman Spellings",
        "description": "Variations in phonetic typing where multiple spellings map to the same phoneme (e.g., 'hai' vs 'he', 'shuru' vs 'suru').",
        "potential_fix": "Incorporate n-gram character language model or context-aware Aksharantar beam search."
    },
    "MULTIPLE_MEANINGS": {
        "name": "Multiple Possible Hindi Words",
        "description": "Homographic Roman words resolving to different native meanings (e.g., 'kal' -> कल yesterday or कल tomorrow).",
        "potential_fix": "Use sentence-level semantic encoder (IndicBERT) or bidirectional context."
    },
    "INCORRECT_SEGMENTATION": {
        "name": "Incorrect Word Segmentation",
        "description": "Roman text written without spaces or with non-standard spacing (e.g., 'karnepadega' instead of 'karne padega').",
        "potential_fix": "Add word-boundary segmentation preprocessing based on Hindi syllabic rules."
    },
    "ENGLISH_TRANSLITERATION": {
        "name": "English Words Incorrectly Transliterated",
        "description": "Common English loan words phonetically converted to Hindi characters instead of retained or normalized.",
        "potential_fix": "Entity extraction and language identification (LID) filter for English loanwords."
    },
    "INCORRECT_MATRA": {
        "name": "Incorrect Matras / Diacritics",
        "description": "Subtle vowel length or nasalization errors (e.g., 'ू' vs 'ु', 'ी' vs 'ि', missing chandrabindu / anusvara).",
        "potential_fix": "Devanagari post-processing dictionary alignment and spell-check normalization."
    },
    "SEMANTIC_DRIFT": {
        "name": "Grammar Correction Changing Meaning",
        "description": "Generative model alters named entities, numbers, or author's pragmatic tone while attempting correction.",
        "potential_fix": "Strict prompt engineering with entity preservation constraints and low generation temperature."
    },
    "CONTEXT_LOSS_TRANSLATION": {
        "name": "Translation Losing Contextual Meaning",
        "description": "Machine translation producing literal word-for-word output missing colloquial or polite connotations.",
        "potential_fix": "Fine-tuning IndicTrans2 on conversational domain and colloquial parallel corpora."
    },
    "OOV_WORDS": {
        "name": "Out-of-Vocabulary (OOV) / Slang Words",
        "description": "Campus slang, acronyms, or non-standard Roman constructs not found in standard training datasets.",
        "potential_fix": "Dynamic Hinglish lexicon expansion and subword byte-pair tokenization."
    }
}


def diagnose_transliteration_error(
    input_text: str, ref_hindi: str, pred_hindi: str
) -> Dict[str, Any]:
    """
    Diagnoses potential failure modes between reference and predicted Hindi text.
    """
    if ref_hindi.strip() == pred_hindi.strip():
        return {"category": "CORRECT", "explanation": "Perfect match with reference."}

    # Check for matra variations
    def strip_matras(s: str) -> str:
        # Unicode range for Devanagari vowel signs: \u093e - \u094c, \u0901, \u0902
        import re
        return re.sub(r"[\u0901-\u0903\u093e-\u094d]", "", s)

    if strip_matras(ref_hindi) == strip_matras(pred_hindi):
        return {
            "category_key": "INCORRECT_MATRA",
            "category_name": ERROR_CATEGORIES["INCORRECT_MATRA"]["name"],
            "explanation": "Consonants matched accurately, but vowel matras or nasalization signs differed.",
            "suggestion": ERROR_CATEGORIES["INCORRECT_MATRA"]["potential_fix"]
        }

    # Check for English loan words
    common_english = {"ai", "ml", "pdf", "zoom", "report", "project", "class", "meeting"}
    words_in_input = set(input_text.lower().split())
    if words_in_input.intersection(common_english):
        return {
            "category_key": "ENGLISH_TRANSLITERATION",
            "category_name": ERROR_CATEGORIES["ENGLISH_TRANSLITERATION"]["name"],
            "explanation": "Input contains English loan words that may have undergone phonetic conversion.",
            "suggestion": ERROR_CATEGORIES["ENGLISH_TRANSLITERATION"]["potential_fix"]
        }

    # Default category: Ambiguous phonetic spelling
    return {
        "category_key": "AMBIGUOUS_SPELLING",
        "category_name": ERROR_CATEGORIES["AMBIGUOUS_SPELLING"]["name"],
        "explanation": "Phonetic mapping ambiguity between Roman orthography and Devanagari representation.",
        "suggestion": ERROR_CATEGORIES["AMBIGUOUS_SPELLING"]["potential_fix"]
    }


def generate_failure_analysis_report(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes full evaluation test results and groups failures into taxonomic categories.
    """
    category_counts = {k: 0 for k in ERROR_CATEGORIES}
    category_counts["OTHER"] = 0
    failure_cases = []

    for item in test_results:
        ref = item.get("reference_hindi", "")
        pred = item.get("predicted_hindi", "")
        inp = item.get("input_hinglish", "")
        
        if ref.strip() != pred.strip():
            diag = diagnose_transliteration_error(inp, ref, pred)
            cat_key = diag.get("category_key", "OTHER")
            if cat_key in category_counts:
                category_counts[cat_key] += 1
            else:
                category_counts["OTHER"] += 1
                
            failure_cases.append({
                "id": item.get("id"),
                "input": inp,
                "expected": ref,
                "predicted": pred,
                "category": diag.get("category_name", "Phonetic Mismatch"),
                "explanation": diag.get("explanation"),
                "suggestion": diag.get("suggestion")
            })

    return {
        "total_failures": len(failure_cases),
        "category_breakdown": category_counts,
        "sample_failure_cases": failure_cases[:10]  # top 10 diagnostic samples
    }
