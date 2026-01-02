from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_tlt import router as tlt_router
from app.core.config import FRONTEND_ORIGIN

app = FastAPI(title="TLT OCT System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tlt_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
