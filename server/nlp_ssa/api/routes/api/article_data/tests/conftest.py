import pytest

from models.article_data import ArticleData
from models.article_data.factories import ArticleDataFactory
from models.stock.factories import StockFactory
from utils.testing_mocks import get_may_the_4th


@pytest.fixture
def mock_stocks(mock_db_session):
    ntdof_stock = StockFactory(quote_stock_symbol="NTDOF")
    tsla_stock = StockFactory(quote_stock_symbol="TSLA")

    mock_db_session.commit()

    return ntdof_stock, tsla_stock


@pytest.fixture
def mock_ntdof_article_data(mock_db_session, mock_stocks):
    ntdof_stock, _ = mock_stocks

    may_the_4th = get_may_the_4th()

    ntdof_article_data = [
        ArticleDataFactory(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-11),
        ),
        ArticleDataFactory(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-17),
        ),
        ArticleDataFactory(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-20),
        ),
        ArticleDataFactory(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-23),
        ),
        ArticleDataFactory(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-30),
        ),
        ArticleDataFactory(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-50),
        ),
        ArticleDataFactory(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
        ),
    ]

    mock_db_session.commit()

    return [ArticleData.model_validate(ad) for ad in ntdof_article_data]


@pytest.fixture
def mock_tsla_article_data(mock_db_session, mock_stocks):
    _, tsla_stock = mock_stocks

    may_the_4th = get_may_the_4th()

    tsla_article_data = [
        ArticleDataFactory(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-6),
        ),
        ArticleDataFactory(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-12),
        ),
        ArticleDataFactory(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-13),
        ),
        ArticleDataFactory(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-18),
        ),
        ArticleDataFactory(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-22),
        ),
        ArticleDataFactory(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-29),
        ),
        ArticleDataFactory(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            updated_at=may_the_4th.shift(days=-37),
        ),
    ]

    mock_db_session.commit()

    return [ArticleData.model_validate(ad) for ad in tsla_article_data]
