from __future__ import annotations
from typing import Dict, List
import numpy as np

from app.core.config import NUM_DAYS
from app.models.rife_wrapper import interpolate_pair_rife
from app.services.alignment import align_pair

def interpolate_volume(
    day1_frames: List[np.ndarray],
    day30_frames: List[np.ndarray],
    num_days: int = NUM_DAYS,
) -> Dict[int, List[np.ndarray]]:
    """
    For each B-scan index, generate a list of frames over num_days.
    Returns dict: {line_index: [day1, day2, ..., dayN]}.
    """
    assert len(day1_frames) == len(day30_frames)
    num_lines = len(day1_frames)
    # Endpoints included, so intermediate frames = num_days - 2
    num_intermediate = max(num_days - 2, 0)

    line_to_frames: Dict[int, List[np.ndarray]] = {}

    for idx in range(num_lines):
        img1, img2 = align_pair(day1_frames[idx], day30_frames[idx])
        frames = interpolate_pair_rife(img1, img2, num_intermediate)
        # 1-based index for clinicians
        line_to_frames[idx + 1] = frames

    return line_to_frames
