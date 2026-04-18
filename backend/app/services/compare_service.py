from app.services.analysis_service import analyze_stock
from app.services.llm_analysis import _extract_text
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


def _score_total(stock: dict) -> float:
    scores = [
        stock.get("valuation_score"),
        stock.get("trend_score"),
        stock.get("news_score"),
        stock.get("risk_score"),
    ]
    valid_scores = [s for s in scores if s is not None]
    if not valid_scores:
        return -1
    return sum(valid_scores) / len(valid_scores)


def compare_stocks(ticker_1: str, ticker_2: str, risk_level: str, horizon: str) -> dict:
    stock_1 = analyze_stock(ticker_1, risk_level)
    stock_2 = analyze_stock(ticker_2, risk_level)

    score_1 = _score_total(stock_1)
    score_2 = _score_total(stock_2)

    if score_1 == -1 and score_2 == -1:
        better_pick = "Unavailable"
    elif score_1 > score_2:
        better_pick = stock_1["ticker"]
    elif score_2 > score_1:
        better_pick = stock_2["ticker"]
    else:
        better_pick = "Tie"

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0.3
        )

        prompt = ChatPromptTemplate.from_template("""
You are a professional financial analyst.

Compare these two stocks for a {risk_level} risk investor with a {horizon} horizon.

STOCK 1:
Ticker: {ticker_1}
Summary: {summary_1}
Recommendation: {recommendation_1}
Valuation Score: {valuation_1}
Trend Score: {trend_1}
News Score: {news_1}
Risk Score: {risk_1}

STOCK 2:
Ticker: {ticker_2}
Summary: {summary_2}
Recommendation: {recommendation_2}
Valuation Score: {valuation_2}
Trend Score: {trend_2}
News Score: {news_2}
Risk Score: {risk_2}

Better pick from scoring: {better_pick}

Rules:
- Explain the main difference between the two
- Mention which one looks stronger and why
- Mention risk considerations
- Keep it short (4-6 lines)
- Return plain text only
""")

        chain = prompt | llm
        result = chain.invoke({
            "ticker_1": stock_1["ticker"],
            "summary_1": stock_1["summary"],
            "recommendation_1": stock_1["recommendation"],
            "valuation_1": stock_1.get("valuation_score"),
            "trend_1": stock_1.get("trend_score"),
            "news_1": stock_1.get("news_score"),
            "risk_1": stock_1.get("risk_score"),
            "ticker_2": stock_2["ticker"],
            "summary_2": stock_2["summary"],
            "recommendation_2": stock_2["recommendation"],
            "valuation_2": stock_2.get("valuation_score"),
            "trend_2": stock_2.get("trend_score"),
            "news_2": stock_2.get("news_score"),
            "risk_2": stock_2.get("risk_score"),
            "better_pick": better_pick,
            "risk_level": risk_level,
            "horizon": horizon
        })

        comparison_summary = _extract_text(result)

    except Exception:
        comparison_summary = "AI comparison summary is temporarily unavailable."

    return {
        "stock_1": stock_1,
        "stock_2": stock_2,
        "better_pick": better_pick,
        "comparison_summary": comparison_summary
    }