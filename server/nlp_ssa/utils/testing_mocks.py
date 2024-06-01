import arrow


def get_mock_utcnow():
    """Return arrow date for April 1st, 2024 UTC"""
    return arrow.get(2024, 4, 1).to("utc")
