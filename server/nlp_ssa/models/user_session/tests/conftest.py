import pytest

from models.user import UserFacade
from models.user_session import UserSessionFacade


@pytest.fixture
def user_facade(mock_db_session):
    return UserFacade(db_session=mock_db_session)


@pytest.fixture
def user_session_facade(mock_db_session):
    return UserSessionFacade(db_session=mock_db_session)
