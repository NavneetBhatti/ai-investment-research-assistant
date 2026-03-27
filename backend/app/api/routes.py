from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to AI Investment Research Assistant API"
    }


@router.post("/analyze")
def analyze():
    return {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "summary": "Mock response - backend working correctly.",
        "valuation_score": 7,
        "trend_score": 8,
        "news_score": 6,
        "risk_score": 5,
        "recommendation": "Hold",
        "confidence": 7,
        "reasons": [
            "Price trend is currently stable.",
            "Recent news is mixed.",
            "Valuation is reasonable but not deeply discounted."
        ]
    }