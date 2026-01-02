from __future__ import annotations
from pathlib import Path
from typing import List

import cv2
import numpy as np

def load_bscan_stack_png(folder: Path) -> List[np.ndarray]:
    """
    Load B-scan PNGs from a folder as grayscale uint8 images,
    sorted by filename.
    """
    image_paths = sorted(folder.glob("*.png"))
    frames: List[np.ndarray] = []
    for p in image_paths:
        img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        frames.append(img)
    return frames

def normalize_bscan(img: np.ndarray) -> np.ndarray:
    """
    Simple histogram equalization to enhance OCT contrast.
    """
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    return img

def preprocess_volume(folder: Path) -> List[np.ndarray]:
    """
    Full preprocessing pipeline for a volume represented as a folder of PNGs.
    Replace this with DICOM-based loading if needed.
    """
    raw = load_bscan_stack_png(folder)
    return [normalize_bscan(f) for f in raw]
