from __future__ import annotations
from typing import List
import uuid
from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.core.config import SESSIONS_DIR, VIDEO_OUTPUT_DIR
from app.schemas.tlt import TLTProcessResponse, LineVideoInfo
from app.services.preprocessing import preprocess_volume
from app.services.interpolation import interpolate_volume
from app.services.video_generator import generate_video_from_frames

router = APIRouter(prefix="/tlt", tags=["tlt"])

@router.post("/process", response_model=TLTProcessResponse)
async def process_oct_volumes(
    day1_zip: UploadFile = File(..., description="Day-1 OCT volume (folder/zip)"),
    day30_zip: UploadFile = File(..., description="Day-30 OCT volume (folder/zip)"),
):
    """
    Upload Day-1 and Day-30 OCT volumes and generate per-line time-lapse videos.
    CURRENT ASSUMPTION:
      - You upload archives or folders that are already extracted to contain 25 PNGs.
      - In a real system, you would unzip and load DICOM here.
    """
    session_id = str(uuid.uuid4())
    session_dir = SESSIONS_DIR / session_id
    day1_dir = session_dir / "day1"
    day30_dir = session_dir / "day30"
    day1_dir.mkdir(parents=True, exist_ok=True)
    day30_dir.mkdir(parents=True, exist_ok=True)

    # For now, just save raw files to folders.
    # In a real setup, detect zip and extract, or ingest DICOM.
    day1_path = day1_dir / day1_zip.filename
    day30_path = day30_dir / day30_zip.filename

    with day1_path.open("wb") as f:
        shutil.copyfileobj(day1_zip.file, f)
    with day30_path.open("wb") as f:
        shutil.copyfileobj(day30_zip.file, f)

    day1_zip.file.close()
    day30_zip.file.close()

    # TODO: if these are zip files, unzip into day1_dir / day30_dir here.

    # For now, assume PNGs already in day1_dir and day30_dir.
    day1_frames = preprocess_volume(day1_dir)
    day30_frames = preprocess_volume(day30_dir)

    if not day1_frames or not day30_frames:
        raise HTTPException(
            status_code=400,
            detail="No B-scan images found in uploaded volumes.",
        )

    if len(day1_frames) != len(day30_frames):
        raise HTTPException(
            status_code=400,
            detail="Day-1 and Day-30 volumes must have the same number of B-scans.",
        )

    line_to_frames = interpolate_volume(day1_frames, day30_frames)

    # Generate videos per line
    session_video_dir = VIDEO_OUTPUT_DIR / session_id
    session_video_dir.mkdir(parents=True, exist_ok=True)

    for line_index, frames in line_to_frames.items():
        generate_video_from_frames(
            frames,
            session_id=session_id,
            line_index=line_index,
        )

    return TLTProcessResponse(
        session_id=session_id,
        num_lines=len(line_to_frames),
    )

@router.get("/lines", response_model=List[LineVideoInfo])
def list_line_videos(session_id: str):
    """
    List all available B-scan line videos for a session.
    """
    session_video_dir = VIDEO_OUTPUT_DIR / session_id
    if not session_video_dir.exists():
        raise HTTPException(status_code=404, detail="Invalid session_id")

    infos: List[LineVideoInfo] = []

    for line_dir in sorted(session_video_dir.glob("line_*")):
        name = line_dir.name  # line_01, line_02, ...
        try:
            line_str = name.split("_")[1]
            line_index = int(line_str)
        except (IndexError, ValueError):
            continue

        video_path = line_dir / "timelapse.mp4"
        if video_path.exists():
            infos.append(
                LineVideoInfo(
                    line_index=line_index,
                    video_url=f"/tlt/video?session_id={session_id}&line_index={line_index}",
                )
            )

    return infos

@router.get("/video")
def get_line_video(session_id: str, line_index: int):
    """
    Stream a single B-scan line time-lapse video.
    """
    video_path = (
        VIDEO_OUTPUT_DIR
        / session_id
        / f"line_{line_index:02d}"
        / "timelapse.mp4"
    )

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(str(video_path), media_type="video/mp4")
