"""
Model utility helpers for device placement, memory safety, and model caching.
"""

import gc
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def get_gpu_memory_info() -> Dict[str, Any]:
    """Returns GPU memory usage statistics if CUDA is available."""
    try:
        import torch
        if torch.cuda.is_available():
            total = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            allocated = torch.cuda.memory_allocated(0) / (1024 ** 3)
            reserved = torch.cuda.memory_reserved(0) / (1024 ** 3)
            return {
                "available": True,
                "name": torch.cuda.get_device_name(0),
                "total_gb": round(total, 2),
                "allocated_gb": round(allocated, 2),
                "reserved_gb": round(reserved, 2),
                "free_gb": round(total - reserved, 2)
            }
    except Exception as e:
        logger.debug(f"GPU check error: {e}")
    return {"available": False}


def clear_gpu_cache():
    """Forces garbage collection and clears PyTorch CUDA memory cache."""
    try:
        import torch
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
    except Exception as e:
        logger.debug(f"Cache clear error: {e}")


def safe_device(preferred: str = "auto") -> str:
    """
    Selects the safe compute device ('cuda' or 'cpu').
    If CUDA has less than 1.0 GB free VRAM, defaults to 'cpu' to prevent OOM.
    """
    if preferred == "cpu":
        return "cpu"
    try:
        import torch
        if torch.cuda.is_available():
            info = get_gpu_memory_info()
            if info.get("available") and info.get("free_gb", 0) >= 0.8:
                return "cuda"
            else:
                logger.warning("Low VRAM detected (< 0.8 GB). Falling back to CPU for safety.")
                return "cpu"
    except Exception:
        pass
    return "cpu"
