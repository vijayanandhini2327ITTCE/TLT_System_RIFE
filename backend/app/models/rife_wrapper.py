from __future__ import annotations
from typing import List
import numpy as np

from ccvfi import AutoModel, ConfigType  # RIFE-based VFI library [web:41][web:60]

# Singleton instance
_rife_model = None

def get_rife_model():
    global _rife_model
    if _rife_model is None:
        # Use a pretrained RIFE config; adjust as needed [web:41][web:60]
        _rife_model = AutoModel(
            model_name=ConfigType.RIFE_IFNet_v426_slow,  # quality-focused preset
        )
    return _rife_model

def interpolate_pair_rife(
    img0: np.ndarray,
    img1: np.ndarray,
    num_intermediate: int,
) -> List[np.ndarray]:
    """
    Use RIFE (via ccvfi) to interpolate between two B-scans.
    Returns [img0, mid1, ..., midN, img1] as uint8 images.
    """
    model = get_rife_model()
    # ccvfi works directly on uint8 HxWxC or HxW arrays [web:41]
    frames = model.interpolate(img0, img1, num_intermediate)
    # Ensure list[ndarray]
    return [np.array(f, copy=False) for f in frames]
