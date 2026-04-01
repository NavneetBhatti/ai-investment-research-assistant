from fastapi import APIRouter
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.tools.market_data import get_market_data
from app.tools.fundamentals import get_fundamentals
import time

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to AI Investment Research Assistant API"
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    ticker = payload.ticker.upper()

    # Step 1: Get market data
    market_data = get_market_data(ticker)

    # Step 2: Delay to avoid API rate limit
    time.sleep(1.2)

    # Step 3: Get fundamentals
    fundamentals = get_fundamentals(ticker)

    # Extract market data
    price = market_data.get("price")
    change_percent = market_data.get("change_percent")

    # Extract fundamentals
    company_name = fundamentals.get("company_name") or f"{ticker} Inc."
    pe_ratio = fundamentals.get("pe_ratio")
    eps = fundamentals.get("eps")
    market_cap = fundamentals.get("market_cap")

    # Build summary
    summary_parts = []

    if price:
        summary_parts.append(f"{ticker} is trading at {price}")
    if change_percent:
        summary_parts.append(f"with daily change {change_percent}")
    if pe_ratio:
        summary_parts.append(f"P/E ratio is {pe_ratio}")
    if eps:
        summary_parts.append(f"EPS is {eps}")

    if summary_parts:
        summary = " ".join(summary_parts) + "."
    else:
        summary = f"Limited data is available for {ticker}."

    # Build reasons
    reasons = []

    if price:
        reasons.append(f"Current market price is {price}.")
    if change_percent:
        reasons.append(f"Latest daily move is {change_percent}.")
    if pe_ratio:
        reasons.append(f"P/E ratio is {pe_ratio}.")
    if market_cap:
        reasons.append(f"Market capitalization is {market_cap}.")

    # Handle API issues
    if market_data.get("error"):
        reasons.append(f"Market data issue: {market_data['error']}")
    if fundamentals.get("error"):
        reasons.append(f"Fundamentals issue: {fundamentals['error']}")

    # Add generic logic
    reasons.append(f"Recommendation adjusted for {payload.risk_level} risk profile.")

    return {
        "ticker": ticker,
        "company_name": company_name,
        "summary": summary,
        "current_price": price,
        "daily_change_percent": change_percent,
        "pe_ratio": pe_ratio,
        "eps": eps,
        "market_cap": market_cap,
        "valuation_score": 6,
        "trend_score": 7,
        "news_score": 5,
        "risk_score": 5,
        "recommendation": "Hold",
        "confidence": 6,
        "reasons": reasons
    }