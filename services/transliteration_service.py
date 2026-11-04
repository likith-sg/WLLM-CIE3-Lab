"""
Service layer for Roman Hinglish to Devanagari Hindi transliteration.
Encapsulates business logic, caching, and model orchestration.
"""

import time
import logging
from typing import Dict, Any
from models.indicxlit import IndicXlitModel
from config.settings import INDICXLIT_MODEL_ID

logger = logging.getLogger(__name__)

class TransliterationService:
    """Manages transliteration operations."""

    def __init__(self, model: IndicXlitModel = None):
        self.model = model or IndicXlitModel(model_id=INDICXLIT_MODEL_ID)

    def transliterate(self, roman_text: str) -> Dict[str, Any]:
        """
        Executes transliteration and captures latency and metadata.
        """
        if not roman_text or not roman_text.strip():
            return {
                "success": False,
                "error": "Empty input text provided.",
                "input_text": "",
                "devanagari_text": "",
                "latency_ms": 0.0,
                "model_info": self.model.get_info()
            }

        start_time = time.perf_counter()
        try:
            devanagari = self.model.transliterate_sentence(roman_text)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "success": True,
                "input_text": roman_text,
                "devanagari_text": devanagari,
                "latency_ms": round(elapsed_ms, 2),
                "model_info": self.model.get_info()
            }
        except Exception as e:
            logger.error(f"Transliteration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "input_text": roman_text,
                "devanagari_text": "",
                "latency_ms": 0.0,
                "model_info": self.model.get_info()
            }
