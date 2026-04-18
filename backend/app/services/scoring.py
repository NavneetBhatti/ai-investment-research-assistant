def safe_float(value, default=None):
    try:
        if value is None or value == "None" or value == "":
            return default
        return float(str(value).replace("%", "").replace(",", ""))
    except Exception:
        return default


def calculate_news_sentiment(news: list) -> dict:
    positive_keywords = [
        "beat", "beats", "growth", "strong", "surge", "record", "gain", "gains",
        "up", "upgrade", "bullish", "profit", "profits", "expands", "expansion"
    ]
    negative_keywords = [
        "miss", "misses", "drop", "falls", "down", "downgrade", "bearish",
        "loss", "losses", "lawsuit", "risk", "cuts", "decline", "weak"
    ]

    if not news:
        return {
            "news_score": None,
            "sentiment_label": None
        }

    score = 0
    usable_news_found = False

    for item in news:
        title = item.get("title", "").lower()
        if not title:
            continue

        if "rate limit" in title or "api key" in title or "failed" in title or "error" in title:
            continue

        usable_news_found = True

        for word in positive_keywords:
            if word in title:
                score += 1

        for word in negative_keywords:
            if word in title:
                score -= 1

    if not usable_news_found:
        return {
            "news_score": None,
            "sentiment_label": None
        }

    if score >= 2:
        return {"news_score": 8, "sentiment_label": "Positive"}
    if score == 1:
        return {"news_score": 6, "sentiment_label": "Slightly Positive"}
    if score == 0:
        return {"news_score": 5, "sentiment_label": "Neutral"}
    if score == -1:
        return {"news_score": 4, "sentiment_label": "Slightly Negative"}

    return {"news_score": 3, "sentiment_label": "Negative"}


def calculate_scores(market_data: dict, fundamentals: dict, news: list) -> dict:
    valuation_score = None
    trend_score = None
    risk_score = None

    change_percent = safe_float(market_data.get("change_percent"))
    pe_ratio = safe_float(fundamentals.get("pe_ratio"))
    eps = safe_float(fundamentals.get("eps"))
    market_cap = safe_float(fundamentals.get("market_cap"))

    if pe_ratio is not None:
        if pe_ratio < 15:
            valuation_score = 8
        elif pe_ratio < 25:
            valuation_score = 7
        elif pe_ratio < 35:
            valuation_score = 6
        else:
            valuation_score = 4

    if change_percent is not None:
        if change_percent > 2:
            trend_score = 8
        elif change_percent > 0:
            trend_score = 7
        elif change_percent > -2:
            trend_score = 5
        else:
            trend_score = 3

    news_result = calculate_news_sentiment(news)
    news_score = news_result["news_score"]
    sentiment_label = news_result["sentiment_label"]

    if eps is not None or market_cap is not None:
        risk_score = 5
        if eps is not None and eps > 0:
            risk_score += 1
        if market_cap is not None:
            if market_cap > 200_000_000_000:
                risk_score += 1
            elif market_cap < 2_000_000_000:
                risk_score -= 1
        risk_score = max(1, min(risk_score, 10))

    available_scores = [
        score for score in [valuation_score, trend_score, news_score, risk_score]
        if score is not None
    ]

    if not available_scores:
        recommendation = "Insufficient Data"
        confidence = None
    else:
        average_score = round(sum(available_scores) / len(available_scores))
        confidence = average_score

        if len(available_scores) < 2:
            recommendation = "Insufficient Data"
        elif average_score >= 7:
            recommendation = "Buy"
        elif average_score >= 5:
            recommendation = "Hold"
        else:
            recommendation = "Avoid"

    return {
        "valuation_score": valuation_score,
        "trend_score": trend_score,
        "news_score": news_score,
        "risk_score": risk_score,
        "recommendation": recommendation,
        "confidence": confidence,
        "news_sentiment": sentiment_label
    }