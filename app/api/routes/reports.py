import os
from fastapi import APIRouter, HTTPException
from app.core.config import REPORTS_DIR

router = APIRouter()


@router.get("/reports/{analysis_id}")
def get_report(analysis_id: str):

    report_path = os.path.join(REPORTS_DIR, f"{analysis_id}.json")

    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found")

    with open(report_path, "r", encoding="utf-8") as f:
        return f.read()