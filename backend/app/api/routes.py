from fastapi import APIRouter
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to AI Investment Research Assistant API"
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    ticker = payload.ticker.upper()

    return {
        "ticker": ticker,
        "company_name": "Apple Inc." if ticker == "AAPL" else f"{ticker} Inc.",
        "summary": f"Mock analysis for {ticker} with {payload.horizon} horizon and {payload.risk_level} risk profile.",
        "valuation_score": 7,
        "trend_score": 8,
        "news_score": 6,
        "risk_score": 5,
        "recommendation": "Hold",
        "confidence": 7,
        "reasons": [
            f"{ticker} shows stable momentum in this mock example.",
            "Recent news sentiment is mixed.",
            f"Recommendation is adjusted for a {payload.risk_level} risk investor."
        ]
    }