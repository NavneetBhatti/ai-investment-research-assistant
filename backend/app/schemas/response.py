from typing import List
from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    ticker: str
    company_name: str
    summary: str
    valuation_score: int
    trend_score: int
    news_score: int
    risk_score: int
    recommendation: str
    confidence: int
    reasons: List[str]