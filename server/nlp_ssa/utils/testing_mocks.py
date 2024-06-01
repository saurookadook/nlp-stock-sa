import arrow


def get_mock_utcnow():
    return arrow.get(2024, 4, 1).to("utc")
