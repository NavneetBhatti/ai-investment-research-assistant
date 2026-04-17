from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


def _extract_text(result) -> str:
    if result is None:
        return "AI analysis is temporarily unavailable."

    content = getattr(result, "content", result)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text_value = item.get("text")
                if text_value:
                    parts.append(text_value)
        if parts:
            return "\n".join(parts)

    return str(content)


def generate_ai_analysis(data: dict) -> str:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0.3
        )

        prompt = ChatPromptTemplate.from_template("""
You are a professional financial analyst.

Explain this stock decision clearly.

DATA:
Ticker: {ticker}
Price: {price}
Change: {change}
P/E: {pe_ratio}
EPS: {eps}
Market Cap: {market_cap}

Scores:
Valuation: {valuation_score}
Trend: {trend_score}
News: {news_score}
Risk: {risk_score}

Recommendation: {recommendation}
Risk Profile: {risk_level}

Rules:
- Explain why
- Mention strengths and weaknesses
- Keep it short (3-4 lines)
- Return plain text only
""")

        chain = prompt | llm

        result = chain.invoke({
            "ticker": data.get("ticker"),
            "price": data.get("price"),
            "change": data.get("change"),
            "pe_ratio": data.get("pe_ratio"),
            "eps": data.get("eps"),
            "market_cap": data.get("market_cap"),
            "valuation_score": data.get("valuation_score"),
            "trend_score": data.get("trend_score"),
            "news_score": data.get("news_score"),
            "risk_score": data.get("risk_score"),
            "recommendation": data.get("recommendation"),
            "risk_level": data.get("risk_level")
        })

        return _extract_text(result)

    except Exception as error:
        return f"AI analysis is temporarily unavailable: {str(error)}"