from typing import List, Optional
from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    source: Optional[str] = None
    published_at: Optional[str] = None


class AnalyzeResponse(BaseModel):
    ticker: str
    company_name: str
    summary: str
    current_price: Optional[str] = None
    daily_change_percent: Optional[str] = None
    pe_ratio: Optional[str] = None
    eps: Optional[str] = None
    market_cap: Optional[str] = None
    news_sentiment: Optional[str] = None
    valuation_score: Optional[int] = None
    trend_score: Optional[int] = None
    news_score: Optional[int] = None
    risk_score: Optional[int] = None
    recommendation: str
    confidence: Optional[int] = None
    reasons: List[str]
    news: List[NewsItem] = []
    ai_analysis: Optional[str] = None