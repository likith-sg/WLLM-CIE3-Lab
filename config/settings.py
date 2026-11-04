"""
Configuration settings for the Hinglish Smart Writing Assistant.
Manages paths, model IDs, device resolution, and feature defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if available
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Hardware & Execution Environment
CONFIGURED_DEVICE = os.getenv("INFERENCE_DEVICE", "auto").lower()

def resolve_device() -> str:
    """
    Resolves the execution device ('cuda' or 'cpu') based on availability
    and safety constraints (4GB RTX 3050 VRAM management).
    """
    if CONFIGURED_DEVICE == "cpu":
        return "cpu"
    try:
        import torch
        if torch.cuda.is_available():
            # Check available VRAM (RTX 3050 has ~4GB)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            return "cuda"
    except Exception:
        pass
    return "cpu"

DEVICE = resolve_device()

# Official AI4Bharat & BharatGen Model Identifiers
INDICXLIT_MODEL_ID = os.getenv(
    "INDICXLIT_MODEL_ID", "ai4bharat/indicxlit-en-indic-v1.0"
)
INDICTRANS2_MODEL_ID = os.getenv(
    "INDICTRANS2_MODEL_ID", "ai4bharat/indictrans2-indic-en-dist-200M"
)
PARAM1_MODEL_ID = os.getenv(
    "BHARATGEN_PARAM1_MODEL_ID", "bharatgenai/Param-1-2.9B-Instruct"
)

# Enhancement Provider ('param1', 'gemini', 'rule_hybrid')
WRITING_PROVIDER = os.getenv("WRITING_ENHANCEMENT_PROVIDER", "param1")

# Paths
DATA_DIR = BASE_DIR / "data"
EVALUATION_DIR = BASE_DIR / "evaluation"
TEST_DATASET_PATH = EVALUATION_DIR / "test_dataset.json"

# Translation language codes
SRC_LANG_HINDI = "hin_Deva"
TGT_LANG_ENGLISH = "eng_Latn"

# Curated Sample Hinglish Inputs covering various communicative categories
SAMPLE_INPUTS = [
    {
        "category": "Everyday Conversation",
        "label": "Daily Greetings & Well-being",
        "text": "mera naam likith hai aur mai bangalore me rehta hu"
    },
    {
        "category": "Education / College",
        "label": "Assignment Submission Query",
        "text": "kya aap mujhe assignment submit karne ki last date bata sakte ho?"
    },
    {
        "category": "Professional Communication",
        "label": "Meeting Reschedule Request",
        "text": "aaj ki meeting postpone karke kal subah 10 baje rakh sakte hai kya?"
    },
    {
        "category": "Questions",
        "label": "Inquiry on Class Schedule",
        "text": "kal hamari data science ki class kitne baje shuru hogi?"
    },
    {
        "category": "Commands and Requests",
        "label": "Urgent File Request",
        "text": "kripya project report ki pdf file jaldi bhej dijiye"
    },
    {
        "category": "Mixed Hindi-English Expressions",
        "label": "Tech & Commute Conversation",
        "text": "traffic bohot heavy tha isliye conference call attend nahi kar paya"
    },
    {
        "category": "Long Sentence",
        "label": "Complex Project Explanation",
        "text": "hum artificial intelligence aur natural language processing ka use karke Indian languages ke liye ek smart tool bana rahe hai"
    },
    {
        "category": "Ambiguous Roman Spellings",
        "label": "Multi-word Roman Spelling",
        "text": "mai kal sham ko market jaunga aur kuch naye kapde khareedunga"
    }
]
