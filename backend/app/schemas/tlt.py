from __future__ import annotations
from pydantic import BaseModel

class TLTProcessResponse(BaseModel):
    session_id: str
    num_lines: int

class LineVideoInfo(BaseModel):
    line_index: int
    video_url: str
