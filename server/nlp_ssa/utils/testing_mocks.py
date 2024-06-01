import arrow


def get_mock_utcnow():
    """Return arrow date for April 1st, 2024 UTC"""
    return arrow.get(2024, 4, 1).to("utc")


def get_may_the_4th():
    """Return arrow date for May 4th, 2024 UTC"""
    return arrow.get(2024, 5, 4).to("utc")
