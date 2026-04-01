def format_currency_number(value):
    try:
        num = float(value)
        return f"{num:.2f}"
    except (TypeError, ValueError):
        return value


def format_percent(value):
    try:
        text = str(value).replace("%", "").strip()
        num = float(text)
        return f"{num:.2f}%"
    except (TypeError, ValueError):
        return value


def format_market_cap(value):
    try:
        num = float(value)

        if num >= 1_000_000_000_000:
            return f"{num / 1_000_000_000_000:.2f}T"
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B"
        if num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"

        return f"{num:.2f}"
    except (TypeError, ValueError):
        return value