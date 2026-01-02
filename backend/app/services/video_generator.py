from __future__ import annotations
from pathlib import Path
from typing import List

import cv2
import ffmpeg
import numpy as np

from app.core.config import VIDEO_OUTPUT_DIR, DEFAULT_FPS

def save_frames_to_temp_dir(frames: List[np.ndarray], tmp_dir: Path) -> None:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for i, frame in enumerate(frames):
        if frame.ndim == 2:
            out = frame
        else:
            out = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out_path = tmp_dir / f"frame_{i:04d}.png"
        cv2.imwrite(str(out_path), out)

def generate_video_from_frames(
    frames: List[np.ndarray],
    session_id: str,
    line_index: int,
    fps: int = DEFAULT_FPS,
) -> Path:
    """
    Saves frames to temp dir and uses ffmpeg to create MP4.
    """
    session_video_dir = VIDEO_OUTPUT_DIR / session_id
    line_dir = session_video_dir / f"line_{line_index:02d}"
    tmp_dir = line_dir / "tmp"

    line_dir.mkdir(parents=True, exist_ok=True)

    save_frames_to_temp_dir(frames, tmp_dir)

    output_path = line_dir / "timelapse.mp4"

    (
        ffmpeg
        .input(str(tmp_dir / "frame_%04d.png"), framerate=fps)
        .output(
            str(output_path),
            vcodec="libx264",
            pix_fmt="yuv420p",
            r=fps,
        )
        .overwrite_output()
        .run(quiet=True)
    )

    # You can remove tmp_dir here if desired
    return output_path
