def safe_float(value, default=None):
    try:
        if value is None or value == "None" or value == "":
            return default
        return float(str(value).replace("%", "").replace(",", ""))
    except Exception:
        return default


def calculate_scores(market_data: dict, fundamentals: dict, news: list) -> dict:
    valuation_score = 5
    trend_score = 5
    news_score = 5
    risk_score = 5

    price = safe_float(market_data.get("price"))
    change_percent = safe_float(market_data.get("change_percent"))
    pe_ratio = safe_float(fundamentals.get("pe_ratio"))
    eps = safe_float(fundamentals.get("eps"))
    market_cap = safe_float(fundamentals.get("market_cap"))

    # Valuation scoring
    if pe_ratio is not None:
        if pe_ratio < 15:
            valuation_score = 8
        elif pe_ratio < 25:
            valuation_score = 7
        elif pe_ratio < 35:
            valuation_score = 6
        else:
            valuation_score = 4

    # Trend scoring
    if change_percent is not None:
        if change_percent > 2:
            trend_score = 8
        elif change_percent > 0:
            trend_score = 7
        elif change_percent > -2:
            trend_score = 5
        else:
            trend_score = 3

    # News scoring
    if news:
        first_title = news[0].get("title", "").lower() if isinstance(news[0], dict) else ""
        if "failed" in first_title or "thank you for using alpha vantage" in first_title:
            news_score = 4
        else:
            news_score = 6 if len(news) >= 3 else 5

    # Risk scoring
    if eps is not None and eps > 0:
        risk_score += 1
    if market_cap is not None:
        if market_cap > 200_000_000_000:
            risk_score += 1
        elif market_cap < 2_000_000_000:
            risk_score -= 1

    risk_score = max(1, min(risk_score, 10))

    total_score = valuation_score + trend_score + news_score + risk_score
    average_score = round(total_score / 4)

    if average_score >= 7:
        recommendation = "Buy"
    elif average_score >= 5:
        recommendation = "Hold"
    else:
        recommendation = "Avoid"

    confidence = average_score

    return {
        "valuation_score": valuation_score,
        "trend_score": trend_score,
        "news_score": news_score,
        "risk_score": risk_score,
        "recommendation": recommendation,
        "confidence": confidence
    }