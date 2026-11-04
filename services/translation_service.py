"""
Service layer for Hindi-to-English translation using IndicTrans2.
"""

import time
import logging
from typing import Dict, Any
from models.indictrans2 import IndicTrans2Model
from config.settings import INDICTRANS2_MODEL_ID

logger = logging.getLogger(__name__)

class TranslationService:
    """Manages translation operations."""

    def __init__(self, model: IndicTrans2Model = None):
        self.model = model or IndicTrans2Model(model_id=INDICTRANS2_MODEL_ID)

    def translate(self, hindi_text: str) -> Dict[str, Any]:
        """
        Translates Hindi text to English and captures performance telemetry.
        """
        if not hindi_text or not hindi_text.strip():
            return {
                "success": False,
                "error": "Empty text provided for translation.",
                "hindi_text": "",
                "english_text": "",
                "latency_ms": 0.0,
                "model_info": self.model.get_info()
            }

        start_time = time.perf_counter()
        try:
            english = self.model.translate(hindi_text)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "success": True,
                "hindi_text": hindi_text,
                "english_text": english,
                "latency_ms": round(elapsed_ms, 2),
                "model_info": self.model.get_info()
            }
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "hindi_text": hindi_text,
                "english_text": "",
                "latency_ms": 0.0,
                "model_info": self.model.get_info()
            }
