import pytest
from uuid import UUID

from constants import (
    AuthProviderEnum,
    TokenTypeEnum,
    EIGHT_HOURS_IN_SECONDS,
    SIX_MONTHS_IN_SECONDS,
)
from models.user import UserFacade
from models.user_session import UserSessionFacade


@pytest.fixture
def expected_user_dict():
    return dict(
        id=UUID("4c26429c-c8e8-4fc6-9b39-357d3e5e7dd6"),
        username="billy-the-butcher",
        first_name="Billy",
        last_name="Butcher",
    )


@pytest.fixture
def expected_user_session_dict():
    return dict(
        id=UUID("5a3c4dcb-e7f7-4160-b58f-52c97eb4ae91"),
        access_token="ghu_66289c7b82e290132d4c9fd1a82a5ad1b630",
        auth_provider=AuthProviderEnum.GITHUB,
        expires_in=EIGHT_HOURS_IN_SECONDS,
        refresh_token="ghr_lmao2e3ab0370f447256f2e25ba170e77a1c866a640fae85b08ef900081209b99165a788fe61",
        refresh_token_expires_in=SIX_MONTHS_IN_SECONDS,
        token_type=TokenTypeEnum.BEARER,
        # scope="",
    )


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
