import pytest

from models.user import UserFacade, UserFactory


@pytest.fixture
def user_facade(mock_db_session):
    return UserFacade(db_session=mock_db_session)


def test_get_one_by_id(mock_db_session, user_facade):
    mock_user = UserFactory()
    mock_db_session.commit()

    result = user_facade.get_one_by_id(id=mock_user.id)

    assert result == mock_user


def test_get_one_by_id_no_result(user_facade):
    with pytest.raises(UserFacade.NoResultFound):
        user_facade.get_one_by_id(id="415c5a59-942b-4f08-acb5-2c16f2b37c9b")


def test_get_one_by_username(mock_db_session, user_facade):
    mock_user = UserFactory()
    mock_db_session.commit()

    result = user_facade.get_one_by_username(username=mock_user.username)

    assert result == mock_user


def test_get_one_by_username_no_result(user_facade):
    with pytest.raises(UserFacade.NoResultFound):
        user_facade.get_one_by_username(username="does-not-exist")
