import requests
from app.config import settings


def get_recent_news(ticker: str) -> list:
    ticker = ticker.upper()

    if not settings.ALPHA_VANTAGE_API_KEY:
        return [
            {
                "title": "Missing Alpha Vantage API key",
                "source": "system",
                "published_at": None
            }
        ]

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

        print("NEWS RAW RESPONSE:", data)

        if not data:
            return []

        if "Note" in data:
            return [
                {
                    "title": data["Note"],
                    "source": "Alpha Vantage",
                    "published_at": None
                }
            ]

        if "Information" in data:
            return [
                {
                    "title": data["Information"],
                    "source": "Alpha Vantage",
                    "published_at": None
                }
            ]

        if "Error Message" in data:
            return [
                {
                    "title": data["Error Message"],
                    "source": "Alpha Vantage",
                    "published_at": None
                }
            ]

        feed = data.get("feed", [])

        news_items = []
        for item in feed[:5]:
            news_items.append(
                {
                    "title": item.get("title", "No title available"),
                    "source": item.get("source", "Unknown"),
                    "published_at": item.get("time_published")
                }
            )

        return news_items

    except Exception as error:
        return [
            {
                "title": f"News fetch failed: {str(error)}",
                "source": "system",
                "published_at": None
            }
        ]