import arrow
import pytest
from sqlalchemy import select
from uuid import UUID, uuid4

from models.sentiment_analysis import (
    SentimentAnalysis,
    SentimentAnalysisDB,
    SentimentAnalysisFacade,
)
from models.sentiment_analysis.constants import SentimentEnum
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
    mock_stock_1 = StockFactory(quote_stock_symbol="FOO")
    mock_stock_2 = StockFactory(quote_stock_symbol="BAR")
    mock_db_session.commit()

    mock_sentiment_analysis_1 = SentimentAnalysisFactory(
        quote_stock_symbol=mock_stock_1.quote_stock_symbol
    )
    SentimentAnalysisFactory(quote_stock_symbol=mock_stock_2.quote_stock_symbol)
    mock_sentiment_analysis_3 = SentimentAnalysisFactory(
        quote_stock_symbol=mock_stock_1.quote_stock_symbol
    )
    mock_db_session.commit()

    results = sentiment_analysis_facade.get_all_by_stock_symbol(
        mock_stock_1.quote_stock_symbol
    )

    assert results == [
        SentimentAnalysis.model_validate(mock_sentiment_analysis_1),
        SentimentAnalysis.model_validate(mock_sentiment_analysis_3),
    ]


def test_get_all_by_stock_symbol_no_results(sentiment_analysis_facade):
    results = sentiment_analysis_facade.get_all_by_stock_symbol("NOPE")

    assert results == []


def test_create_or_update_new_article_data(mock_db_session, sentiment_analysis_facade):
    StockFactory(quote_stock_symbol="NTDOF")
    mock_db_session.commit()

    sentiment_analysis_dict = {
        "id": uuid4(),
        "quote_stock_symbol": "NTDOF",
        "source_group_id": UUID("3a0e5f09-3904-46df-bffb-13f5a95412ad"),
        "score": 0.9,
        "sentiment": SentimentEnum.POSITIVE,
    }

    result = sentiment_analysis_facade.create_or_update(payload=sentiment_analysis_dict)

    assert result.quote_stock_symbol == sentiment_analysis_dict.get(
        "quote_stock_symbol"
    )
    assert result.source_group_id == sentiment_analysis_dict.get("source_group_id")
    assert result.score == sentiment_analysis_dict.get("score")
    assert result.sentiment == sentiment_analysis_dict.get("sentiment")
    # TODO: find better way to mock server 'now' function
    assert isinstance(result.created_at, arrow.Arrow)
    assert isinstance(result.updated_at, arrow.Arrow)


def test_create_or_update_existing_article_data(
    mock_db_session, sentiment_analysis_facade
):
    mock_stock = StockFactory(quote_stock_symbol="DIS")
    mock_db_session.commit()

    mock_sentiment_analysis = SentimentAnalysisFactory(
        id=UUID("7fb2c6c5-b2e3-4bd0-9b84-22fbeb729d8c"),
        quote_stock_symbol=mock_stock.quote_stock_symbol,
        score=0.5,
    )
    mock_db_session.commit()

    updated_sentiment_analysis_dict = {
        "id": mock_sentiment_analysis.id,
        "quote_stock_symbol": mock_sentiment_analysis.quote_stock_symbol,
        "source_group_id": mock_sentiment_analysis.source_group_id,
        "score": 0.9,
        "sentiment": SentimentEnum.POSITIVE,
    }

    sentiment_analysis_facade.create_or_update(payload=updated_sentiment_analysis_dict)
    mock_db_session.commit()

    sentiment_analysis_db = mock_db_session.execute(
        select(SentimentAnalysisDB).where(
            SentimentAnalysisDB.id == updated_sentiment_analysis_dict.get("id")
        )
    ).scalar_one()

    result = SentimentAnalysis.model_validate(sentiment_analysis_db)

    assert result.id == mock_sentiment_analysis.id
    assert result.quote_stock_symbol == mock_sentiment_analysis.quote_stock_symbol
    assert result.source_group_id == mock_sentiment_analysis.source_group_id
    assert result.score == updated_sentiment_analysis_dict.get("score")
    assert result.sentiment == updated_sentiment_analysis_dict.get("sentiment")
    assert result.created_at == get_mock_utcnow()
    # TODO: find better way to mock server 'now' function
    assert isinstance(result.updated_at, arrow.Arrow)
