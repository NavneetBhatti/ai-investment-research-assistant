import requests
from app.config import settings


def get_fundamentals(ticker: str) -> dict:
    ticker = ticker.upper()

    if not settings.ALPHA_VANTAGE_API_KEY:
        return {
            "ticker": ticker,
            "error": "Fundamentals API key is missing"
        }

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
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
                "error": "No fundamentals data found"
            }

        if "Note" in data:
            return {
                "ticker": ticker,
                "error": "Fundamentals data temporarily unavailable due to API rate limits"
            }

        if "Information" in data:
            info_text = data["Information"].lower()
            if "rate limit" in info_text or "api key" in info_text or "25 requests per day" in info_text:
                return {
                    "ticker": ticker,
                    "error": "Fundamentals data temporarily unavailable due to API rate limits"
                }
            return {
                "ticker": ticker,
                "error": "Fundamentals data is currently unavailable"
            }

        if "Error Message" in data:
            return {
                "ticker": ticker,
                "error": "Invalid ticker or fundamentals data not found"
            }

        if "Symbol" not in data:
            return {
                "ticker": ticker,
                "error": "Unexpected fundamentals response"
            }

        return {
            "ticker": ticker,
            "company_name": data.get("Name"),
            "pe_ratio": data.get("PERatio"),
            "eps": data.get("EPS"),
            "market_cap": data.get("MarketCapitalization"),
            "profit_margin": data.get("ProfitMargin"),
            "analyst_target_price": data.get("AnalystTargetPrice"),
            "sector": data.get("Sector"),
            "industry": data.get("Industry"),
            "source": "Alpha Vantage"
        }

    except Exception:
        return {
            "ticker": ticker,
            "error": "Fundamentals request failed"
        }