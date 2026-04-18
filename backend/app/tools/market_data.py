import requests
from app.config import settings


def get_market_data(ticker: str) -> dict:
    ticker = ticker.upper()

    if not settings.ALPHA_VANTAGE_API_KEY:
        return {
            "ticker": ticker,
            "error": "Market data API key is missing"
        }

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not data:
            return {
                "ticker": ticker,
                "error": "No market data found"
            }

        if "Note" in data:
            return {
                "ticker": ticker,
                "error": "Market data temporarily unavailable due to API rate limits"
            }

        if "Information" in data:
            info_text = data["Information"].lower()
            if "rate limit" in info_text or "api key" in info_text or "25 requests per day" in info_text:
                return {
                    "ticker": ticker,
                    "error": "Market data temporarily unavailable due to API rate limits"
                }
            return {
                "ticker": ticker,
                "error": "Market data is currently unavailable"
            }

        quote = data.get("Global Quote", {})

        if not quote:
            return {
                "ticker": ticker,
                "error": "No market data found"
            }

        return {
            "ticker": ticker,
            "price": quote.get("05. price"),
            "change": quote.get("09. change"),
            "change_percent": quote.get("10. change percent"),
            "volume": quote.get("06. volume"),
            "latest_trading_day": quote.get("07. latest trading day"),
            "previous_close": quote.get("08. previous close"),
            "source": "Alpha Vantage"
        }

    except Exception:
        return {
            "ticker": ticker,
            "error": "Market data request failed"
        }