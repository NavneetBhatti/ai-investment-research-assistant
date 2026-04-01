import requests
from app.config import settings


def get_market_data(ticker: str) -> dict:
    ticker = ticker.upper()

    if not settings.ALPHA_VANTAGE_API_KEY:
        return {
            "ticker": ticker,
            "error": "Missing Alpha Vantage API key"
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

    except Exception as error:
        return {
            "ticker": ticker,
            "error": str(error)
        }