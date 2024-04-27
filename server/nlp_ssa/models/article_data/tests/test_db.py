import arrow
import pytest
from sqlalchemy import select, and_
from unittest import mock
from uuid import UUID

from models.article_data import ArticleDataDB, ArticleDataFactory


@pytest.fixture(autouse=True)
def mock_utcnow():
    mock.patch("arrow.utcnow", return_value=arrow.get(2024, 3, 11))
    return mock_utcnow


@pytest.fixture
def expected_article_data_dict():
    return dict(
        id=UUID("4c26429c-c8e8-4fc6-9b39-357d3e5e7dd6"),
        quote_stock_symbol="NTDOF",
        source_group_id=UUID("3a0e5f09-3904-46df-bffb-13f5a95412ad"),
        source_url="https://finance.yahoo.com/news/they-are-killin-it-123459876.html",
        raw_content="meow meow meow meow meow meow business meow meow meow business business",
        sentence_tokens="                              business                business business",
    )


def test_article_data_db(mock_db_session, expected_article_data_dict):
    mock_article_data = ArticleDataFactory(**expected_article_data_dict)
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(ArticleDataDB).where(
            and_(
                ArticleDataDB.id == mock_article_data.id,
                ArticleDataDB.quote_stock_symbol
                == mock_article_data.quote_stock_symbol,
            )
        )
    ).scalar_one()

    assert result.id == expected_article_data_dict["id"]
    assert result.quote_stock_symbol == expected_article_data_dict["quote_stock_symbol"]
    assert result.source_group_id == expected_article_data_dict["source_group_id"]
    assert result.source_url == expected_article_data_dict["source_url"]
    assert result.raw_content == expected_article_data_dict["raw_content"]
    assert result.sentence_tokens == expected_article_data_dict["sentence_tokens"]
    assert result.created_at == arrow.get(2020, 4, 15).to("utc")
    assert result.updated_at == arrow.get(2020, 4, 15).to("utc")
