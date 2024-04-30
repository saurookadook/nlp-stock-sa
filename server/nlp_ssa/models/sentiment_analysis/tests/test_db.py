import arrow
import pytest
from sqlalchemy import select, and_
from unittest import mock
from uuid import UUID

from models.sentiment_analysis import (
    SentimentAnalysisDB,
    SentimentEnum,
)
from models.sentiment_analysis.factories import SentimentAnalysisFactory
from models.stock.factories import StockFactory


@pytest.fixture(autouse=True)
def mock_utcnow():
    mock.patch("arrow.utcnow", return_value=arrow.get(2024, 3, 11))
    return mock_utcnow


@pytest.fixture
def expected_sentiment_analysis_dict():
    return dict(
        id=UUID("4c26429c-c8e8-4fc6-9b39-357d3e5e7dd6"),
        source_group_id=UUID("16ec77ca-7dd0-483d-be53-f625618d66ab"),
        quote_stock_symbol="CATZ",
        score=20.9,
        sentiment=SentimentEnum.POSITIVE.value,
    )


def test_sentiment_analysis_db(mock_db_session, expected_sentiment_analysis_dict):
    mock_quote_stock_symbol = expected_sentiment_analysis_dict["quote_stock_symbol"]
    StockFactory(quote_stock_symbol=mock_quote_stock_symbol)
    mock_db_session.commit()

    sentiment_analysis = SentimentAnalysisFactory(**expected_sentiment_analysis_dict)
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(SentimentAnalysisDB).where(
            and_(
                SentimentAnalysisDB.id == sentiment_analysis.id,
                SentimentAnalysisDB.quote_stock_symbol == mock_quote_stock_symbol,
            )
        )
    ).scalar_one()

    assert result.id == expected_sentiment_analysis_dict["id"]
    assert result.source_group_id == expected_sentiment_analysis_dict["source_group_id"]
    assert (
        result.quote_stock_symbol
        == expected_sentiment_analysis_dict["quote_stock_symbol"]
    )
    assert result.score == expected_sentiment_analysis_dict["score"]
    assert result.sentiment.value == expected_sentiment_analysis_dict["sentiment"]
    assert result.created_at == arrow.get(2020, 4, 15)
    assert result.updated_at == arrow.get(2020, 4, 15)
