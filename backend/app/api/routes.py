from fastapi import APIRouter
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.tools.market_data import get_market_data
from app.tools.fundamentals import get_fundamentals
from app.tools.news import get_recent_news
from app.services.scoring import calculate_scores
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

    market_data = get_market_data(ticker)
    time.sleep(1.2)

    fundamentals = get_fundamentals(ticker)
    time.sleep(1.2)

    news = get_recent_news(ticker)

    scores = calculate_scores(
        market_data=market_data,
        fundamentals=fundamentals,
        news=news
    )

    price = market_data.get("price")
    change_percent = market_data.get("change_percent")

    company_name = fundamentals.get("company_name") or f"{ticker} Inc."
    pe_ratio = fundamentals.get("pe_ratio")
    eps = fundamentals.get("eps")
    market_cap = fundamentals.get("market_cap")

    summary_parts = []

    if price:
        summary_parts.append(f"{ticker} is trading at {price}")
    if change_percent:
        summary_parts.append(f"with daily change {change_percent}")
    if pe_ratio:
        summary_parts.append(f"P/E ratio is {pe_ratio}")
    if eps:
        summary_parts.append(f"EPS is {eps}")
    if news and len(news) > 0 and "failed" not in news[0]["title"].lower():
        summary_parts.append(f"Recent news items found: {len(news)}")

    if summary_parts:
        summary = " ".join(summary_parts) + "."
    else:
        summary = f"Limited data is available for {ticker}."

    reasons = []

    if price:
        reasons.append(f"Current market price is {price}.")
    if change_percent:
        reasons.append(f"Latest daily move is {change_percent}.")
    if pe_ratio:
        reasons.append(f"P/E ratio is {pe_ratio}.")
    if market_cap:
        reasons.append(f"Market capitalization is {market_cap}.")
    if news and len(news) > 0:
        reasons.append(f"Fetched {len(news)} recent news items.")

    if market_data.get("error"):
        reasons.append(f"Market data issue: {market_data['error']}")
    if fundamentals.get("error"):
        reasons.append(f"Fundamentals issue: {fundamentals['error']}")

    reasons.append(f"Recommendation adjusted for {payload.risk_level} risk profile.")
    reasons.append(f"Valuation score computed as {scores['valuation_score']}/10.")
    reasons.append(f"Trend score computed as {scores['trend_score']}/10.")
    reasons.append(f"News score computed as {scores['news_score']}/10.")
    reasons.append(f"Risk score computed as {scores['risk_score']}/10.")

    return {
        "ticker": ticker,
        "company_name": company_name,
        "summary": summary,
        "current_price": price,
        "daily_change_percent": change_percent,
        "pe_ratio": pe_ratio,
        "eps": eps,
        "market_cap": market_cap,
        "valuation_score": scores["valuation_score"],
        "trend_score": scores["trend_score"],
        "news_score": scores["news_score"],
        "risk_score": scores["risk_score"],
        "recommendation": scores["recommendation"],
        "confidence": scores["confidence"],
        "reasons": reasons,
        "news": news
    }