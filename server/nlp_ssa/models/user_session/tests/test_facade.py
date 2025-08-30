import arrow
import pytest
from uuid import UUID, uuid4

from constants import AuthProviderEnum
from models.user import User, UserFacade
from models.user.factories import UserFactory
from models.user_session import UserSession, UserSessionFacade
from models.user_session.factories import UserSessionFactory


def test_get_one_by_id(mock_db_session, user_session_facade: UserSessionFacade):
    test_user = UserFactory()
    mock_db_session.commit()

    test_user_session = UserSessionFactory(user_id=test_user.id)
    mock_db_session.commit()

    result = user_session_facade.get_one_by_id(test_user_session.id)

    assert result == UserSession.model_validate(test_user_session)


def test_get_first_by_user_id_and_auth_provider(
    mock_db_session, user_session_facade: UserSessionFacade
):
    test_user = UserFactory()
    mock_db_session.commit()

    test_user_session = UserSessionFactory(user_id=test_user.id)
    mock_db_session.commit()

    result = user_session_facade.get_first_by_user_id_and_auth_provider(
        user_id=test_user.id, auth_provider=AuthProviderEnum.GITHUB.value
    )

    assert result == UserSession.model_validate(test_user_session)


def test_get_first_by_user_id_and_auth_provider_no_result(
    mock_db_session, user_session_facade: UserSessionFacade
):
    user = UserFactory()
    mock_db_session.commit()

    result = user_session_facade.get_first_by_user_id_and_auth_provider(
        user_id=user.id, auth_provider=AuthProviderEnum.GITHUB.value
    )

    assert result == None
