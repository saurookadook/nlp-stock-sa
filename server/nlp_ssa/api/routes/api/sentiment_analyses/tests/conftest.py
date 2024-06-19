import pytest

from models.sentiment_analysis import SentimentAnalysis
from models.sentiment_analysis.factories import SentimentAnalysisFactory


@pytest.fixture
def mock_sentiment_analyses_as_db_models(
    mock_db_session, mock_ntdof_article_data_as_db_models
):
    sentiment_analyses_mocks = []

    for article_data in mock_ntdof_article_data_as_db_models:
        mock_sa = SentimentAnalysisFactory(
            quote_stock_symbol=article_data.quote_stock_symbol,
            source=article_data.polymorphic_source,
        )
        mock_db_session.commit()
        sentiment_analyses_mocks.append(mock_sa)

    return sentiment_analyses_mocks


@pytest.fixture
def mock_sentiment_analyses(mock_sentiment_analyses_as_db_models):
    return [
        SentimentAnalysis.model_validate(sa)
        for sa in mock_sentiment_analyses_as_db_models
    ]
