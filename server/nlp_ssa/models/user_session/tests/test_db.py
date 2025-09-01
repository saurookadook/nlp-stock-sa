import arrow
from sqlalchemy import select, and_
from uuid import UUID

from models.user.factories import UserFactory
from models.user_session import UserSessionDB
from models.user_session.factories import UserSessionFactory


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
