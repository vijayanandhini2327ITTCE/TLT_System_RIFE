from __future__ import annotations
import cv2
import numpy as np

def align_pair(img1: np.ndarray, img2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    ECC-based global registration between two B-scans.
    Returns (aligned_img1, aligned_img2).
    """
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    sz = img1.shape
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (
        cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
        50,
        1e-6,
    )

    try:
        _, warp_matrix = cv2.findTransformECC(
            img1,
            img2,
            warp_matrix,
            cv2.MOTION_EUCLIDEAN,
            criteria,
        )
        aligned2 = cv2.warpAffine(
            img2,
            warp_matrix,
            (sz[1], sz[0]),
            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
        )
        return img1, aligned2
    except cv2.error:
        # If registration fails, return original
        return img1, img2
