from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
SESSIONS_DIR = DATA_DIR / "sessions"
VIDEO_OUTPUT_DIR = BASE_DIR / "videos"

# Ensure base dirs exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# CORS
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

# Interpolation settings
NUM_DAYS = 30        # Day-1 to Day-30 inclusive
DEFAULT_FPS = 30     # Base fps for "normal" playback
