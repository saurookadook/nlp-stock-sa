import pytest

from models.user import UserFacade
from models.user_session import UserSessionFacade


@pytest.fixture
def mock_user_facade_now(mocker, mock_utcnow):
    mock_user_facade_utcnow = mocker.patch("nlp_ssa.models.user.facade.arrow.utcnow")
    mock_user_facade_utcnow.return_value = mock_utcnow


@pytest.fixture
def mock_user_facade_now(mocker, mock_utcnow):
    mock_user_session_facade_utcnow = mocker.patch(
        "nlp_ssa.models.user_session.facade.arrow.utcnow"
    )
    mock_user_session_facade_utcnow.return_value = mock_utcnow


@pytest.fixture
def user_facade(mock_db_session):
    return UserFacade(db_session=mock_db_session)


@pytest.fixture
def user_session_facade(mock_db_session):
    return UserSessionFacade(db_session=mock_db_session)
