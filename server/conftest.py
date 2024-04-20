import arrow
import os
import pytest
import requests_mock
from alembic import command, config
from sqlalchemy.exc import InvalidRequestError
from starlette.testclient import TestClient

from api.app import app
from db import db_session, engine, db_session_dependency
from models.user import UserFactory


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
        # db_connection.close()
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
    return arrow.get(2024, 4, 19).to("utc")


@pytest.fixture(autouse=True)
def mock_arrow_utcnow(mocker, mock_utcnow):
    utcnow_patch = mocker.patch("arrow.utcnow")
    utcnow_patch.return_value = mock_utcnow


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
