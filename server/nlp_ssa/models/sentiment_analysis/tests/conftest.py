import pytest

from models.sentiment_analysis import SentimentAnalysisFacade


@pytest.fixture
def sentiment_analysis_facade(mock_db_session):
    return SentimentAnalysisFacade(db_session=mock_db_session)
