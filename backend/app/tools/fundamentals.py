def get_fundamentals(ticker: str) -> dict:
    return {
        "ticker": ticker.upper(),
        "pe_ratio": None,
        "market_cap": None,
        "revenue_growth": None,
        "source": "mock"
    }