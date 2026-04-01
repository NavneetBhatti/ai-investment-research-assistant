from fastapi import APIRouter
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.tools.market_data import get_market_data
from app.tools.fundamentals import get_fundamentals
from app.tools.news import get_recent_news
from app.services.scoring import calculate_scores
from app.services.formatters import format_currency_number, format_percent, format_market_cap
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

    raw_price = market_data.get("price")
    raw_change_percent = market_data.get("change_percent")

    company_name = fundamentals.get("company_name") or f"{ticker} Inc."
    raw_pe_ratio = fundamentals.get("pe_ratio")
    raw_eps = fundamentals.get("eps")
    raw_market_cap = fundamentals.get("market_cap")

    price = format_currency_number(raw_price) if raw_price else None
    change_percent = format_percent(raw_change_percent) if raw_change_percent else None
    pe_ratio = format_currency_number(raw_pe_ratio) if raw_pe_ratio else None
    eps = format_currency_number(raw_eps) if raw_eps else None
    market_cap = format_market_cap(raw_market_cap) if raw_market_cap else None

    summary_parts = []

    if price:
        summary_parts.append(f"{ticker} is trading at {price}")
    if change_percent:
        summary_parts.append(f"with daily change {change_percent}")
    if pe_ratio:
        summary_parts.append(f"P/E ratio is {pe_ratio}")
    if eps:
        summary_parts.append(f"EPS is {eps}")
    if scores.get("news_sentiment"):
        summary_parts.append(f"News sentiment appears {scores['news_sentiment'].lower()}")

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
    if scores.get("news_sentiment"):
        reasons.append(f"Detected {scores['news_sentiment'].lower()} news sentiment.")

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
        "news_sentiment": scores["news_sentiment"],
        "valuation_score": scores["valuation_score"],
        "trend_score": scores["trend_score"],
        "news_score": scores["news_score"],
        "risk_score": scores["risk_score"],
        "recommendation": scores["recommendation"],
        "confidence": scores["confidence"],
        "reasons": reasons,
        "news": news
    }