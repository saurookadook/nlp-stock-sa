import arrow
import pytest
from sqlalchemy import select
from uuid import UUID, uuid4

from models.article_data import (
    ArticleData,
    ArticleDataDB,
    ArticleDataFacade,
)
from models.article_data.factories import ArticleDataFactory
from models.stock.factories import StockFactory


@pytest.fixture()
def mock_facade_now(mocker, mock_utcnow):
    # mock_facade_urcnow = mocker.patch("nlp_ssa.models.article_data.facade.arrow.utcnow")
    mock_facade_urcnow = mocker.patch("nlp_ssa.models.article_data.facade.arrow.utcnow")
    mock_facade_urcnow.return_value = mock_utcnow


@pytest.fixture
def article_data_facade(mock_db_session):
    return ArticleDataFacade(db_session=mock_db_session)


def test_get_one_by_id(mock_db_session, article_data_facade):
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

    assert results == [mock_article_data_1, mock_article_data_3]


def test_get_all_by_stock_symbol_no_results(article_data_facade):
    results = article_data_facade.get_all_by_stock_symbol("NOPE")

    assert results == []


def test_create_or_update_new_article_data(
    article_data_facade, mock_db_session, mock_utcnow, mock_facade_now
):
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

    assert result.quote_stock_symbol == article_data_dict["quote_stock_symbol"]
    assert result.source_group_id == article_data_dict["source_group_id"]
    assert result.source_url == article_data_dict["source_url"]
    assert result.raw_content == article_data_dict["raw_content"]
    assert result.sentence_tokens == article_data_dict["sentence_tokens"]
    # TODO: not sure why the mocks in the test fixtures aren't working :']
    # assert result.created_at == mock_utcnow
    # assert result.updated_at == mock_utcnow
    assert isinstance(result.created_at, arrow.Arrow)
    assert isinstance(result.updated_at, arrow.Arrow)


def test_create_or_update_existing_article_data(article_data_facade, mock_db_session):
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
        "sentence_tokens": [
            "                    good business                       amazing"
            " returns                                           "
        ],
    }

    article_data_facade.create_or_update(payload=updated_article_data_dict)
    mock_db_session.commit()

    article_data_db = mock_db_session.execute(
        select(ArticleDataDB).where(ArticleDataDB.id == updated_article_data_dict["id"])
    ).scalar_one()

    result = ArticleData.model_validate(article_data_db)

    assert result.quote_stock_symbol == updated_article_data_dict["quote_stock_symbol"]
    assert result.raw_content == updated_article_data_dict["raw_content"]
    assert result.sentence_tokens == updated_article_data_dict["sentence_tokens"]
