import os
import pytest
import requests_mock
from alembic import command, config
from sqlalchemy.exc import InvalidRequestError
from starlette.testclient import TestClient

from api.app import app
from db import db_session, engine, db_session_dependency
from models.article_data import ArticleData
from models.article_data.factories import ArticleDataFactory
from models.stock.factories import StockFactory
from models.user.factories import UserFactory
from utils.testing_mocks import get_may_the_4th, get_mock_utcnow


def pytest_sessionstart(session):
    os.environ["DATABASE_NAME"] = "test_the_money_maker"

    alembic_ini = os.path.join(os.path.abspath("."), "alembic.ini")
    alembic_config = config.Config(alembic_ini)
    command.upgrade(alembic_config, "head")


def db_session_test():
    # db_connection = engine.connect()
    with engine.connect() as db_connection:
        transaction = db_connection.begin()
        try:
            yield db_session(bind=db_connection)
        except InvalidRequestError as e:
            raise InvalidRequestError(
                str(e) + " Make sure you're using db_session correctly!"
            )
        transaction.rollback()
        db_connection.close()
    db_session.remove()


mock_db_session = pytest.fixture(db_session_test)


@pytest.fixture
def server_api_client(mock_db_session):
    app.dependency_overrides[db_session_dependency] = lambda: mock_db_session
    client = TestClient(app)
    return client


@pytest.fixture
def http_requests_mock():
    with requests_mock.Mocker(real_http=True) as mock:
        yield mock


@pytest.fixture
def mock_utcnow():
    return get_mock_utcnow()


@pytest.fixture(autouse=True)
def mock_arrow_utcnow(mocker):
    return mocker.patch("arrow.utcnow", return_value=get_mock_utcnow())


@pytest.fixture
def mock_user(mock_db_session):
    user = UserFactory(
        id="458eae59-4748-42e5-b894-06cb9a25d6c5",
        username="zerosneezes",
        first_name="Zero",
        last_name="McSneezy",
    )
    mock_db_session.commit()
    # app.dependency_overrides[user_required] = lambda: user
    return user


@pytest.fixture
def mock_stocks(mock_db_session):
    ntdof_stock = StockFactory(quote_stock_symbol="NTDOF")
    tsla_stock = StockFactory(quote_stock_symbol="TSLA")

    mock_db_session.commit()

    return ntdof_stock, tsla_stock


@pytest.fixture
def mock_ntdof_article_data_as_db_models(mock_db_session, mock_stocks):
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

    return ntdof_article_data


@pytest.fixture
def mock_tsla_article_data_as_db_models(mock_db_session, mock_stocks):
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

    return tsla_article_data


@pytest.fixture
def mock_ntdof_article_data(mock_ntdof_article_data_as_db_models):
    return [
        ArticleData.model_validate(ad) for ad in mock_ntdof_article_data_as_db_models
    ]


@pytest.fixture
def mock_tsla_article_data(mock_tsla_article_data_as_db_models):
    return [
        ArticleData.model_validate(ad) for ad in mock_tsla_article_data_as_db_models
    ]
