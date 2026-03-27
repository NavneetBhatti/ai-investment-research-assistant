def get_recent_news(ticker: str) -> list:
    return [
        {
            "title": f"Sample news for {ticker.upper()}",
            "summary": "This is a mock news summary.",
            "source": "mock"
        }
    ]