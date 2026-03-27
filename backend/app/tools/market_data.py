def get_market_data(ticker: str) -> dict:
    return {
        "ticker": ticker.upper(),
        "current_price": None,
        "change_percent": None,
        "source": "mock"
    }