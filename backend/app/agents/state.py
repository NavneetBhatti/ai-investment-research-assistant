from typing import List, Dict, Any, TypedDict


class AnalysisState(TypedDict, total=False):
    ticker: str
    horizon: str
    risk_level: str
    market_data: Dict[str, Any]
    fundamentals: Dict[str, Any]
    news_items: List[Dict[str, Any]]
    retrieved_context: List[str]
    analysis_text: str
    scores: Dict[str, int]
    recommendation: str
    confidence: int
    reasons: List[str]
    errors: List[str]