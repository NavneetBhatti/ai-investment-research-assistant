import requests
from app.config import settings


def get_fundamentals(ticker: str) -> dict:
    ticker = ticker.upper()

    if not settings.ALPHA_VANTAGE_API_KEY:
        return {
            "ticker": ticker,
            "error": "Missing Alpha Vantage API key"
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

        print("FUNDAMENTALS RAW RESPONSE:", data)

        if not data:
            return {
                "ticker": ticker,
                "error": "Empty fundamentals response"
            }

        if "Note" in data:
            return {
                "ticker": ticker,
                "error": data["Note"]
            }

        if "Information" in data:
            return {
                "ticker": ticker,
                "error": data["Information"]
            }

        if "Error Message" in data:
            return {
                "ticker": ticker,
                "error": data["Error Message"]
            }

        if "Symbol" not in data:
            return {
                "ticker": ticker,
                "error": f"Unexpected fundamentals response: {data}"
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

    except Exception as error:
        return {
            "ticker": ticker,
            "error": str(error)
        }