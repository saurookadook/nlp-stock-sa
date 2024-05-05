import pytest

from models.sentiment_analysis import (
    SentimentAnalysis,
    SentimentAnalysisFacade,
)
from models.sentiment_analysis.factories import SentimentAnalysisFactory
from models.stock.factories import StockFactory


@pytest.fixture
def sentiment_analysis_facade(mock_db_session):
    return SentimentAnalysisFacade(db_session=mock_db_session)


def test_get_one_by_id(mock_db_session, sentiment_analysis_facade):
    mock_stock = StockFactory()
    mock_db_session.commit()

    mock_sentiment_analysis = SentimentAnalysisFactory(
        quote_stock_symbol=mock_stock.quote_stock_symbol
    )
    mock_db_session.commit()

    result = sentiment_analysis_facade.get_one_by_id(id=mock_sentiment_analysis.id)

    assert result == SentimentAnalysis.model_validate(mock_sentiment_analysis)


def test_get_one_by_id_no_result(sentiment_analysis_facade):
    with pytest.raises(SentimentAnalysisFacade.NoResultFound):
        sentiment_analysis_facade.get_one_by_id(
            id="ba379b11-6c65-4cf9-af09-43c5ae41e979"
        )
