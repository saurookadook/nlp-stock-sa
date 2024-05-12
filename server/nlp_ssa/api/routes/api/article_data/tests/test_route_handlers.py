import arrow
import pytest

from api.routes.api.article_data.route_handlers import (
    get_all_article_data,
    get_article_data_by_stock_slug,
)
from models.article_data import ArticleData
from models.article_data.factories import ArticleDataFactory
from models.stock.factories import StockFactory


@pytest.fixture
def mock_stocks(mock_db_session):
    ntdof_stock = StockFactory(quote_stock_symbol="NTDOF")
    tsla_stock = StockFactory(quote_stock_symbol="TSLA")

    mock_db_session.commit()

    return ntdof_stock, tsla_stock


@pytest.fixture
def mock_ntdof_article_data(mock_db_session, mock_stocks, mock_utcnow):
    ntdof_stock, _ = mock_stocks

    ntdof_article_data_1 = ArticleDataFactory(
        quote_stock_symbol=ntdof_stock.quote_stock_symbol,
        date_modified=mock_utcnow.shift(days=-20),
    )
    ntdof_article_data_2 = ArticleDataFactory(
        quote_stock_symbol=ntdof_stock.quote_stock_symbol,
        date_modified=mock_utcnow.shift(days=-17),
    )
    ntdof_article_data_3 = ArticleDataFactory(
        quote_stock_symbol=ntdof_stock.quote_stock_symbol,
        date_modified=mock_utcnow.shift(days=-11),
    )
    mock_db_session.commit()

    return (ntdof_article_data_1, ntdof_article_data_2, ntdof_article_data_3)


@pytest.fixture
def mock_tsla_article_data(mock_db_session, mock_stocks, mock_utcnow):
    _, tsla_stock = mock_stocks

    tsla_article_data_1 = ArticleDataFactory(
        quote_stock_symbol=tsla_stock.quote_stock_symbol,
        date_modified=mock_utcnow.shift(days=-18),
    )
    tsla_article_data_2 = ArticleDataFactory(
        quote_stock_symbol=tsla_stock.quote_stock_symbol,
        date_modified=mock_utcnow.shift(days=-13),
    )
    tsla_article_data_3 = ArticleDataFactory(
        quote_stock_symbol=tsla_stock.quote_stock_symbol,
        date_modified=mock_utcnow.shift(days=-12),
    )
    tsla_article_data_4 = ArticleDataFactory(
        quote_stock_symbol=tsla_stock.quote_stock_symbol,
        date_modified=mock_utcnow.shift(days=-6),
    )
    mock_db_session.commit()

    return (
        tsla_article_data_1,
        tsla_article_data_2,
        tsla_article_data_3,
        tsla_article_data_4,
    )


def test_get_all_article_data_one_stock(
    mock_db_session, mock_stocks, mock_ntdof_article_data
):
    ntdof_stock, _ = mock_stocks

    ntdof_article_data_1, ntdof_article_data_2, ntdof_article_data_3 = (
        mock_ntdof_article_data
    )

    results = get_all_article_data(db_session=mock_db_session)

    expected = [
        dict(
            stock_symbol=ntdof_stock.quote_stock_symbol,
            data=[
                ArticleData.model_validate(ntdof_article_data_3),
                ArticleData.model_validate(ntdof_article_data_2),
                ArticleData.model_validate(ntdof_article_data_1),
            ],
        )
    ]

    assert results == expected


def test_get_all_article_data_multiple_stocks(
    mock_db_session, mock_stocks, mock_ntdof_article_data, mock_tsla_article_data
):
    ntdof_stock, tsla_stock = mock_stocks
    ntdof_article_data_1, ntdof_article_data_2, ntdof_article_data_3 = (
        mock_ntdof_article_data
    )
    (
        tsla_article_data_1,
        tsla_article_data_2,
        tsla_article_data_3,
        tsla_article_data_4,
    ) = mock_tsla_article_data

    results = get_all_article_data(db_session=mock_db_session)

    expected = [
        dict(
            stock_symbol=tsla_stock.quote_stock_symbol,
            data=[
                ArticleData.model_validate(tsla_article_data_4),
                ArticleData.model_validate(tsla_article_data_3),
                ArticleData.model_validate(tsla_article_data_2),
                ArticleData.model_validate(tsla_article_data_1),
            ],
        ),
        dict(
            stock_symbol=ntdof_stock.quote_stock_symbol,
            data=[
                ArticleData.model_validate(ntdof_article_data_3),
                ArticleData.model_validate(ntdof_article_data_2),
                ArticleData.model_validate(ntdof_article_data_1),
            ],
        ),
    ]

    assert results == expected


def test_get_all_article_data_no_results(mock_db_session):
    results = get_all_article_data(db_session=mock_db_session)

    assert results == []


def test_get_article_data_by_stock_slug(mock_db_session):
    pass


def test_get_article_data_by_stock_slug_multiple_results(mock_db_session):
    pass


def test_get_article_data_by_stock_slug_no_results(mock_db_session):
    pass
