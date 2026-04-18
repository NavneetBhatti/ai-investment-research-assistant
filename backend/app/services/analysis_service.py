from app.tools.market_data import get_market_data
from app.tools.fundamentals import get_fundamentals
from app.tools.news import get_recent_news
from app.services.scoring import calculate_scores
from app.services.formatters import format_currency_number, format_percent, format_market_cap
from app.services.llm_analysis import generate_ai_analysis
import time


def analyze_stock(ticker: str, risk_level: str) -> dict:
    ticker = ticker.upper()

    market_data = {}
    fundamentals = {}
    news = []
    reasons = []

    try:
        market_data = get_market_data(ticker) or {}
    except Exception as error:
        market_data = {"error": f"Market data failed: {str(error)}"}

    time.sleep(1.2)

    try:
        fundamentals = get_fundamentals(ticker) or {}
    except Exception as error:
        fundamentals = {"error": f"Fundamentals failed: {str(error)}"}

    time.sleep(1.2)

    try:
        news = get_recent_news(ticker) or []
    except Exception:
        news = []

    try:
        scores = calculate_scores(
            market_data=market_data,
            fundamentals=fundamentals,
            news=news
        )
    except Exception:
        scores = {
            "valuation_score": None,
            "trend_score": None,
            "news_score": None,
            "risk_score": None,
            "recommendation": "Insufficient Data",
            "confidence": None,
            "news_sentiment": None
        }

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

    if summary_parts:
        summary = " ".join(summary_parts) + "."
    else:
        summary = f"Reliable external data is currently unavailable for {ticker}. Partial analysis only."

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
        reasons.append(f"Recent news sentiment is {scores['news_sentiment'].lower()}.")

    if market_data.get("error"):
        reasons.append(f"Market data issue: {market_data['error']}")
    if fundamentals.get("error"):
        reasons.append(f"Fundamentals issue: {fundamentals['error']}")

    reasons.append(f"Recommendation adjusted for {risk_level} risk profile.")

    if scores.get("valuation_score") is not None:
        reasons.append(f"Valuation score computed as {scores['valuation_score']}/10.")
    if scores.get("trend_score") is not None:
        reasons.append(f"Trend score computed as {scores['trend_score']}/10.")
    if scores.get("news_score") is not None:
        reasons.append(f"News score computed as {scores['news_score']}/10.")
    if scores.get("risk_score") is not None:
        reasons.append(f"Risk score computed as {scores['risk_score']}/10.")

    if scores.get("recommendation") == "Insufficient Data":
        reasons.append("Not enough reliable external data was available to generate a full recommendation.")

    try:
        ai_analysis = generate_ai_analysis({
            "ticker": ticker,
            "price": price,
            "change": change_percent,
            "pe_ratio": pe_ratio,
            "eps": eps,
            "market_cap": market_cap,
            "valuation_score": scores.get("valuation_score"),
            "trend_score": scores.get("trend_score"),
            "news_score": scores.get("news_score"),
            "risk_score": scores.get("risk_score"),
            "recommendation": scores.get("recommendation"),
            "risk_level": risk_level
        })
    except Exception:
        ai_analysis = "AI analysis is temporarily unavailable right now."

    return {
        "ticker": ticker,
        "company_name": company_name,
        "summary": summary,
        "current_price": price,
        "daily_change_percent": change_percent,
        "pe_ratio": pe_ratio,
        "eps": eps,
        "market_cap": market_cap,
        "news_sentiment": scores.get("news_sentiment"),
        "valuation_score": scores.get("valuation_score"),
        "trend_score": scores.get("trend_score"),
        "news_score": scores.get("news_score"),
        "risk_score": scores.get("risk_score"),
        "recommendation": scores.get("recommendation", "Insufficient Data"),
        "confidence": scores.get("confidence"),
        "reasons": reasons,
        "news": news,
        "ai_analysis": ai_analysis
    }