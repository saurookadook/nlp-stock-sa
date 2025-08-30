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


def test_get_one_by_id_no_result(user_session_facade: UserSessionFacade):
    with pytest.raises(UserSessionFacade.NoResultFound):
        user_session_facade.get_one_by_id(id="4c24beca-922f-4f10-819e-37931d949a29")


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
    test_user = UserFactory()
    mock_db_session.commit()

    result = user_session_facade.get_first_by_user_id_and_auth_provider(
        user_id=test_user.id, auth_provider=AuthProviderEnum.GITHUB.value
    )

    assert result == None


def test_get_all_by_user_id(mock_db_session, user_session_facade: UserSessionFacade):
    test_user = UserFactory()
    mock_db_session.commit()

    test_user_session_github = UserSessionFactory(user_id=test_user.id)
    test_user_session_google = UserSessionFactory(
        user_id=test_user.id, auth_provider=AuthProviderEnum.GOOGLE.value
    )
    test_user_session_microsoft = UserSessionFactory(
        user_id=test_user.id, auth_provider=AuthProviderEnum.MICROSOFT.value
    )
    mock_db_session.commit()

    results = user_session_facade.get_all_by_user_id(test_user.id)

    assert UserSession.model_validate(test_user_session_github) in results
    assert UserSession.model_validate(test_user_session_google) in results
    assert UserSession.model_validate(test_user_session_microsoft) in results


def test_get_all_by_user_id_no_results(
    mock_db_session, user_session_facade: UserSessionFacade
):
    test_user = UserFactory()
    mock_db_session.commit()

    results = user_session_facade.get_all_by_user_id(test_user.id)

    assert results == []
