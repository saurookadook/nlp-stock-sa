import arrow
import pytest
import secrets
from rich import inspect
from sqlalchemy.exc import IntegrityError
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


def test_get_one_by_cache_key(mock_db_session, user_session_facade: UserSessionFacade):
    test_user = UserFactory()
    mock_db_session.commit()

    test_user_session = UserSessionFactory(
        cache_key=f"{test_user.username}:{secrets.token_urlsafe(17)}",
        user_id=test_user.id,
    )
    mock_db_session.commit()

    result = user_session_facade.get_one_by_cache_key(test_user_session.cache_key)

    assert result == UserSession.model_validate(test_user_session)


def test_get_one_by_cache_key_no_result(user_session_facade: UserSessionFacade):
    with pytest.raises(UserSessionFacade.NoResultFound):
        user_session_facade.get_one_by_cache_key(
            cache_key=f"not_real:{secrets.token_urlsafe(17)}"
        )


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


def test_create_or_update_new_record(
    mock_db_session,  # force formatting
    expected_user_session_dict,
    user_session_facade: UserSessionFacade,
):
    test_user = UserFactory()
    mock_db_session.commit()

    test_user_session_dict = dict(**expected_user_session_dict, user_id=test_user.id)

    result = user_session_facade.create_or_update(payload=test_user_session_dict)

    for k, v in test_user_session_dict.items():
        assert getattr(result, k) == v


def test_create_or_update_existing_record(
    mock_db_session, expected_user_session_dict, user_session_facade: UserSessionFacade
):
    test_user = UserFactory()
    mock_db_session.commit()

    test_user_session = UserSessionFactory(
        **expected_user_session_dict, user_id=test_user.id
    )
    mock_db_session.commit()

    updated_user_session_dict = {
        "id": test_user_session.id,
        "access_token": "ghu_" + secrets.token_hex(18),
        "refresh_token": "ghr_" + secrets.token_hex(38),
    }

    result = user_session_facade.create_or_update(payload=updated_user_session_dict)
    merged_expected_user_session_dict = {
        **expected_user_session_dict,
        **updated_user_session_dict,
    }

    for k, v in merged_expected_user_session_dict.items():
        assert getattr(result, k) == v


def test_create_or_update_no_user_record_found(
    expected_user_session_dict, user_session_facade: UserSessionFacade
):
    with pytest.raises(IntegrityError):
        user_session_facade.create_or_update(payload=expected_user_session_dict)


def test_delete_one_by_id(mock_db_session, user_session_facade: UserSessionFacade):
    test_user = UserFactory()
    mock_db_session.commit()

    test_user_session = UserSessionFactory(user_id=test_user.id)
    mock_db_session.commit()

    result = user_session_facade.delete_one_by_id(test_user_session.id)

    assert result.id == test_user_session.id
    assert result.user_id == test_user_session.user_id


def test_delete_one_by_id_no_record_found(user_session_facade: UserSessionFacade):
    with pytest.raises(UserSessionFacade.NoResultFound):
        user_session_facade.delete_one_by_id("2cef01cf-a3b9-4abc-a776-ec50dad659b4")
