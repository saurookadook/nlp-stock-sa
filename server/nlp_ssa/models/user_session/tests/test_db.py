import arrow
import pytest
from sqlalchemy import select, and_
from uuid import UUID

from constants import (
    AuthProviderEnum,
    TokenTypeEnum,
    EIGHT_HOURS_IN_SECONDS,
    SIX_MONTHS_IN_SECONDS,
)
from models.user.factories import UserFactory
from models.user_session import UserSessionDB
from models.user_session.factories import UserSessionFactory


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


def test_user_session_db(
    expected_user_dict, expected_user_session_dict, mock_db_session
):
    user = UserFactory(**expected_user_dict)
    mock_db_session.commit()

    user_session = UserSessionFactory(**expected_user_session_dict, user_id=user.id)
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(UserSessionDB).where(
            and_(
                UserSessionDB.id == user_session.id,
                UserSessionDB.user_id == user_session.user_id,
            )
        )
    ).scalar_one()

    assert result.id == expected_user_session_dict["id"]
    assert result.user_id == expected_user_dict["id"]
    assert result.access_token == expected_user_session_dict["access_token"]
    assert result.auth_provider == expected_user_session_dict["auth_provider"]
    assert result.expires_in == expected_user_session_dict["expires_in"]
    assert result.refresh_token == expected_user_session_dict["refresh_token"]
    assert (
        result.refresh_token_expires_in
        == expected_user_session_dict["refresh_token_expires_in"]
    )
    assert result.token_type == expected_user_session_dict["token_type"]
    assert result.created_at == arrow.get(2024, 4, 1).to("utc")
    assert result.updated_at == arrow.get(2024, 4, 1).to("utc")
