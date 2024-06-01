import pytest

from models.user import UserFacade


@pytest.fixture
def user_facade(mock_db_session):
    return UserFacade(db_session=mock_db_session)
