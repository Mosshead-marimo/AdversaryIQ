from pydantic import BaseModel
from typing import List, Dict, Any


class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str


class ReportResponse(BaseModel):
    analysis_id: str
    report: Dict[str, Any]