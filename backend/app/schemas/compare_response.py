from typing import Optional
from pydantic import BaseModel
from app.schemas.response import AnalyzeResponse


class CompareResponse(BaseModel):
    stock_1: AnalyzeResponse
    stock_2: AnalyzeResponse
    better_pick: Optional[str] = None
    comparison_summary: Optional[str] = None