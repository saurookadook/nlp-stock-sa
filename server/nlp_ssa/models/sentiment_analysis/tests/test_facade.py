import pytest
from uuid import UUID

from models.sentiment_analysis import (
    SentimentAnalysis,
    SentimentAnalysisFacade,
)
from models.sentiment_analysis.factories import SentimentAnalysisFactory
from models.stock.factories import StockFactory
from utils.testing_mocks import get_mock_utcnow


def test_get_one_by_id(mock_db_session, sentiment_analysis_facade):
    mock_stock = StockFactory()
    mock_db_session.commit()

    mock_sentiment_analysis = SentimentAnalysisFactory(
        quote_stock_symbol=mock_stock.quote_stock_symbol
    )
    mock_db_session.commit()

    result = sentiment_analysis_facade.get_one_by_id(row_id=mock_sentiment_analysis.id)

    assert result == SentimentAnalysis.model_validate(mock_sentiment_analysis)


def test_get_one_by_id_no_result(sentiment_analysis_facade):
    with pytest.raises(SentimentAnalysisFacade.NoResultFound):
        sentiment_analysis_facade.get_one_by_id(
            row_id="ba379b11-6c65-4cf9-af09-43c5ae41e979"
        )


def test_get_one_by_source_group_id(mock_db_session, sentiment_analysis_facade):
    mock_stock = StockFactory()
    mock_db_session.commit()

    mock_sentiment_analysis = SentimentAnalysisFactory(
        quote_stock_symbol=mock_stock.quote_stock_symbol
    )
    mock_db_session.commit()

    result = sentiment_analysis_facade.get_one_by_source_group_id(
        source_group_id=mock_sentiment_analysis.source_group_id
    )

    assert result == SentimentAnalysis.model_validate(mock_sentiment_analysis)


def test_get_one_by_source_group_id_no_result(sentiment_analysis_facade):
    with pytest.raises(SentimentAnalysisFacade.NoResultFound):
        sentiment_analysis_facade.get_one_by_source_group_id(
            source_group_id=UUID("a7b70a1f-5c64-4647-bb7b-35098b88e620")
        )


def test_get_all_by_stock_symbol(mock_db_session, sentiment_analysis_facade):
    assert "Implement me! :D" is False


def test_get_all_by_stock_symbol_no_results(sentiment_analysis_facade):
    results = sentiment_analysis_facade.get_all_by_stock_symbol("NOPE")

    assert results == []


def test_create_or_update_new_article_data(mock_db_session, sentiment_analysis_facade):
    assert "Implement me! :D" is False


def test_create_or_update_existing_article_data(
    mock_db_session, sentiment_analysis_facade
):
    assert "Implement me! :D" is False
