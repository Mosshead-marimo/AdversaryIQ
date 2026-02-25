import os
import json
from fastapi import APIRouter, HTTPException

router = APIRouter()

REPORT_DIR = os.path.abspath("reports")


@router.get("/reports/{analysis_id}")
def get_report(analysis_id: str):
    report_path = os.path.join(REPORT_DIR, f"{analysis_id}.json")

    if not os.path.isfile(report_path):
        raise HTTPException(status_code=404, detail="Report not found")

    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    return report