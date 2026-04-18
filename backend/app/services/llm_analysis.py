from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.rag.retriever import retrieve_context


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
        # Build retrieval query
        rag_query_parts = [
            f"ticker {data.get('ticker')}",
            f"recommendation {data.get('recommendation')}",
            f"risk profile {data.get('risk_level')}",
            f"valuation score {data.get('valuation_score')}",
            f"trend score {data.get('trend_score')}",
            f"news score {data.get('news_score')}",
            f"risk score {data.get('risk_score')}",
        ]

        rag_query = " ".join([part for part in rag_query_parts if part])

        retrieved_context = retrieve_context(rag_query, k=3)
        rag_context_text = "\n\n".join(retrieved_context)

        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0.3
        )

        prompt = ChatPromptTemplate.from_template("""
You are a professional financial analyst.

Use BOTH:
1. the stock analysis data
2. the retrieved investment knowledge

to generate a grounded explanation.

STOCK DATA:
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

RETRIEVED INVESTMENT KNOWLEDGE:
{rag_context}

Rules:
- Explain why this recommendation was given
- Use the retrieved investment knowledge where relevant
- Mention strengths and weaknesses
- Keep it short (3-5 lines)
- If data is missing, say that clearly
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
            "risk_level": data.get("risk_level"),
            "rag_context": rag_context_text
        })

        return _extract_text(result)

    except Exception as error:
        return f"AI analysis is temporarily unavailable right now: {str(error)}"