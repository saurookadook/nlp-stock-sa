import arrow
import pytest
from sqlalchemy import select
from uuid import UUID, uuid4

from constants import SourceDiscriminatorEnum
from models.article_data import (
    ArticleData,
    ArticleDataDB,
    ArticleDataFacade,
)
from models.article_data.factories import ArticleDataFactory
from models.stock.factories import StockFactory


def test_get_one_by_id(article_data_facade, mock_db_session):
    mock_stock = StockFactory()
    mock_db_session.commit()

    mock_article_data = ArticleDataFactory(
        quote_stock_symbol=mock_stock.quote_stock_symbol
    )
    mock_db_session.commit()

    result = article_data_facade.get_one_by_id(id=mock_article_data.id)

    assert result == ArticleData.model_validate(mock_article_data)


def test_get_one_by_id_no_result(article_data_facade):
    with pytest.raises(ArticleDataFacade.NoResultFound):
        article_data_facade.get_one_by_id(id="2cad8f15-795e-44b8-bf4d-ce81d586594a")


def test_get_one_by_source_url(article_data_facade, mock_db_session):
    mock_stock = StockFactory()
    mock_db_session.commit()

    mock_article_data = ArticleDataFactory(
        quote_stock_symbol=mock_stock.quote_stock_symbol,
        source_url="https://best-news-ever.com/news/article-about-a-stock.html",
    )
    mock_db_session.commit()

    result = article_data_facade.get_one_by_source_url(
        source_url=mock_article_data.source_url
    )

    assert result == ArticleData.model_validate(mock_article_data)


def test_get_one_by_source_url_no_result(article_data_facade):
    with pytest.raises(ArticleDataFacade.NoResultFound):
        article_data_facade.get_one_by_source_url(
            source_url="https://best-news-ever.com/news/does-not-exist.html"
        )


def test_get_all_by_stock_symbol(article_data_facade, mock_db_session):
    mock_stock_1 = StockFactory(quote_stock_symbol="FOO")
    mock_stock_2 = StockFactory(quote_stock_symbol="BAR")
    mock_db_session.commit()

    mock_article_data_1 = ArticleDataFactory(
        quote_stock_symbol=mock_stock_1.quote_stock_symbol
    )
    ArticleDataFactory(quote_stock_symbol=mock_stock_2.quote_stock_symbol)
    mock_article_data_3 = ArticleDataFactory(
        quote_stock_symbol=mock_stock_1.quote_stock_symbol
    )
    mock_db_session.commit()

    results = article_data_facade.get_all_by_stock_symbol(
        mock_stock_1.quote_stock_symbol
    )

    assert results == [
        ArticleData.model_validate(mock_article_data_1),
        ArticleData.model_validate(mock_article_data_3),
    ]


def test_get_all_by_stock_symbol_no_results(article_data_facade):
    results = article_data_facade.get_all_by_stock_symbol("NOPE")

    assert results == []


def test_create_or_update_new_article_data(article_data_facade, mock_db_session):
    StockFactory(quote_stock_symbol="NTDOF")
    mock_db_session.commit()

    article_data_dict = {
        "id": uuid4(),
        "quote_stock_symbol": "NTDOF",
        "source_group_id": UUID("3a0e5f09-3904-46df-bffb-13f5a95412ad"),
        "source_url": "https://finance.yahoo.com/news/they-are-killin-it-123459876.html",
        "raw_content": (
            "meow meow meow meow meow meow business meow meow meow business business meow "
            "business meow meow meow woof woof meow"
        ),
        "sentence_tokens": (
            "                              business                business"
            " business      business                              "
        ),
    }

    result = article_data_facade.create_or_update(payload=article_data_dict)

    assert result.quote_stock_symbol == article_data_dict.get("quote_stock_symbol")
    assert result.source_group_id == article_data_dict.get("source_group_id")
    assert result.source_url == article_data_dict.get("source_url")
    assert result.polymorphic_source.data_type_id == article_data_dict.get("id")
    assert result.polymorphic_source.data_type == SourceDiscriminatorEnum.ArticleDataDB
    assert result.raw_content == article_data_dict.get("raw_content")
    assert result.sentence_tokens == article_data_dict.get("sentence_tokens")
    assert isinstance(result.created_at, arrow.Arrow)
    assert isinstance(result.updated_at, arrow.Arrow)

    assert result.author == ""
    assert result.last_updated_date is None
    assert result.published_date is None
    assert result.title == ""


def test_create_or_update_existing_article_data(
    article_data_facade, mock_db_session, mock_utcnow
):
    mock_stock = StockFactory(quote_stock_symbol="DIS")
    mock_db_session.commit()

    mock_article_data = ArticleDataFactory(
        id=UUID("7fb2c6c5-b2e3-4bd0-9b84-22fbeb729d8c"),
        quote_stock_symbol=mock_stock.quote_stock_symbol,
    )
    mock_db_session.commit()

    updated_article_data_dict = {
        "id": mock_article_data.id,
        "quote_stock_symbol": mock_article_data.quote_stock_symbol,
        "source_group_id": mock_article_data.source_group_id,
        "source_url": mock_article_data.source_url,
        "raw_content": (
            "mickey goofy donald good business star wars theme parks amazing"
            " returns big castle epcot cinderella little mermaid"
        ),
        "sentence_tokens": (
            "                    good business                       amazing"
            " returns                                           "
        ),
        "last_updated_date": mock_utcnow,
        "published_date": mock_utcnow.shift(months=-6),
    }

    article_data_facade.create_or_update(payload=updated_article_data_dict)
    mock_db_session.commit()

    article_data_db = mock_db_session.execute(
        select(ArticleDataDB).where(
            ArticleDataDB.id == updated_article_data_dict.get("id")
        )
    ).scalar_one()

    result = ArticleData.model_validate(article_data_db)

    assert result.quote_stock_symbol == mock_article_data.quote_stock_symbol
    assert result.source_group_id == mock_article_data.source_group_id
    assert result.source_url == mock_article_data.source_url
    assert result.polymorphic_source.data_type_id == mock_article_data.id
    assert result.polymorphic_source.data_type == SourceDiscriminatorEnum.ArticleDataDB
    assert result.raw_content == updated_article_data_dict.get("raw_content")
    assert result.sentence_tokens == updated_article_data_dict.get("sentence_tokens")
    assert isinstance(result.created_at, arrow.Arrow)
    assert isinstance(result.updated_at, arrow.Arrow)

    assert result.author == ""
    assert result.last_updated_date == updated_article_data_dict.get(
        "last_updated_date"
    )
    assert result.published_date == updated_article_data_dict.get("published_date")
    assert result.thumbnail_image_url == ""
    assert result.title == ""
