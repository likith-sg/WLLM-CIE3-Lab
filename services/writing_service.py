"""
Service layer for AI Hindi Writing Enhancement.
Coordinates grammar correction, readability restructuring, and styling.
"""

import time
import logging
from typing import Dict, Any
from models.param1 import BharatGenParam1Model
from config.settings import PARAM1_MODEL_ID, WRITING_PROVIDER

logger = logging.getLogger(__name__)

class WritingEnhancementService:
    """Manages Hindi writing improvement operations."""

    def __init__(self, model: BharatGenParam1Model = None):
        self.model = model or BharatGenParam1Model(
            model_id=PARAM1_MODEL_ID,
            provider=WRITING_PROVIDER
        )

    def improve_writing(self, hindi_text: str) -> Dict[str, Any]:
        """
        Enhances Hindi text, measuring latency and reporting status.
        """
        if not hindi_text or not hindi_text.strip():
            return {
                "success": False,
                "error": "Empty Hindi text provided.",
                "original_text": "",
                "improved_text": "",
                "latency_ms": 0.0,
                "model_info": self.model.get_info()
            }

        start_time = time.perf_counter()
        try:
            improved = self.model.enhance_writing(hindi_text)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "success": True,
                "original_text": hindi_text,
                "improved_text": improved,
                "latency_ms": round(elapsed_ms, 2),
                "model_info": self.model.get_info()
            }
        except Exception as e:
            logger.error(f"Writing enhancement failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_text": hindi_text,
                "improved_text": hindi_text,
                "latency_ms": 0.0,
                "model_info": self.model.get_info()
            }
