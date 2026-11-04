"""
Full End-to-End Orchestration Pipeline for Hinglish Smart Writing Assistant.
Sequentially coordinates:
Roman Hinglish -> IndicXlit -> BharatGen Param-1 -> IndicTrans2 -> English Translation.
"""

import time
import logging
from typing import Dict, Any, Optional
from services.transliteration_service import TransliterationService
from services.writing_service import WritingEnhancementService
from services.translation_service import TranslationService

logger = logging.getLogger(__name__)

class PipelineService:
    """Orchestrates the multi-stage Hinglish processing pipeline."""

    def __init__(
        self,
        xlit_service: Optional[TransliterationService] = None,
        writing_service: Optional[WritingEnhancementService] = None,
        translation_service: Optional[TranslationService] = None
    ):
        self.xlit = xlit_service or TransliterationService()
        self.writing = writing_service or WritingEnhancementService()
        self.translation = translation_service or TranslationService()

    def process_all(
        self,
        roman_input: str,
        apply_enhancement: bool = True
    ) -> Dict[str, Any]:
        """
        Executes the complete end-to-end pipeline:
        1. Roman Hinglish -> Native Devanagari Hindi (IndicXlit)
        2. Native Hindi -> Polished Hindi (BharatGen Param-1) [Optional]
        3. Polished Hindi -> Natural English (IndicTrans2)
        """
        overall_start = time.perf_counter()
        
        # Step 1: Transliteration
        xlit_res = self.xlit.transliterate(roman_input)
        if not xlit_res.get("success"):
            return {
                "success": False,
                "error": f"Transliteration stage failed: {xlit_res.get('error')}",
                "stage_failed": "transliteration",
                "original_input": roman_input,
                "transliterated_hindi": "",
                "improved_hindi": "",
                "english_translation": "",
                "stages": {"xlit": xlit_res}
            }

        transliterated_hindi = xlit_res["devanagari_text"]

        # Step 2: Writing Enhancement
        improved_hindi = transliterated_hindi
        writing_res = None
        if apply_enhancement:
            writing_res = self.writing.improve_writing(transliterated_hindi)
            if writing_res.get("success"):
                improved_hindi = writing_res["improved_text"]
            else:
                logger.warning(f"Enhancement failed: {writing_res.get('error')}. Proceeding with transliterated text.")

        # Step 3: Translation
        trans_res = self.translation.translate(improved_hindi)
        english_translation = trans_res.get("english_text", "")

        total_elapsed_ms = (time.perf_counter() - overall_start) * 1000.0

        return {
            "success": True,
            "original_input": roman_input,
            "transliterated_hindi": transliterated_hindi,
            "improved_hindi": improved_hindi,
            "english_translation": english_translation,
            "stages": {
                "transliteration": xlit_res,
                "writing_enhancement": writing_res,
                "translation": trans_res
            },
            "total_latency_ms": round(total_elapsed_ms, 2)
        }
