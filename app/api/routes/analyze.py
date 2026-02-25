import os
import re
import shutil
import sys
import uuid
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException

sys.path.append(os.path.abspath("../"))

from orchestrator.controller import AnalysisController

router = APIRouter()

UPLOAD_DIR = os.path.abspath("temp_upload")
os.makedirs(UPLOAD_DIR, exist_ok=True)

_WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


def _safe_upload_name(raw_filename: Optional[str]) -> str:
    # Drop any client-supplied directory components.
    original = Path(raw_filename or "sample.bin").name

    # Replace Windows-invalid characters and strip trailing dots/spaces.
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", original).strip(" .")

    if not cleaned:
        cleaned = "sample.bin"

    stem, ext = os.path.splitext(cleaned)
    if stem.upper() in _WINDOWS_RESERVED_NAMES:
        stem = f"{stem}_file"

    safe_base = f"{stem}{ext}" if ext else stem
    return f"{uuid.uuid4()}_{safe_base}"


@router.post("/analyze")
async def analyze_sample(file: UploadFile = File(...)):

    try:
        # Save uploaded file temporarily
        safe_name = _safe_upload_name(file.filename)
        temp_path = os.path.join(UPLOAD_DIR, safe_name)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run full pipeline via controller
        controller = AnalysisController(temp_path)
        result = controller.run()

        return {
            "analysis_id": result["analysis_id"],
            "classification": result["classification"],
            "score": result["score"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
