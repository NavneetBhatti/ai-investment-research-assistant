import requests
from app.config import settings


def get_recent_news(ticker: str) -> list:
    ticker = ticker.upper()

    if not settings.ALPHA_VANTAGE_API_KEY:
        return []

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "limit": 5,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        if not data:
            return []

        if "Note" in data:
            return []

        if "Information" in data:
            info_text = data["Information"].lower()
            if "rate limit" in info_text or "api key" in info_text or "25 requests per day" in info_text:
                return []
            return []

        if "Error Message" in data:
            return []

        feed = data.get("feed", [])
        news_items = []

        for item in feed[:5]:
            title = item.get("title", "No title available")

            if not title:
                continue

            lowered = title.lower()
            if "rate limit" in lowered or "api key" in lowered:
                continue

            news_items.append(
                {
                    "title": title,
                    "source": item.get("source", "Unknown"),
                    "published_at": item.get("time_published")
                }
            )

        return news_items

    except Exception:
        return []