import arrow
import pytest
from sqlalchemy import select, and_
from unittest import mock
from uuid import UUID

from models.user import UserFactory, UserDB


@pytest.fixture(autouse=True)
def mock_utcnow():
    mock.patch("arrow.utcnow", return_value=arrow.get(2024, 3, 11))
    return mock_utcnow


@pytest.fixture
def expected_user_dict():
    return dict(
        id=UUID("4c26429c-c8e8-4fc6-9b39-357d3e5e7dd6"),
        username="billy-the-butcher",
        first_name="Billy",
        last_name="Butcher",
    )


def test_user_db(mock_db_session, expected_user_dict):
    user = UserFactory(**expected_user_dict)
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(UserDB).where(
            and_(UserDB.id == user.id, UserDB.username == user.username)
        )
    ).scalar_one()

    assert result.id == expected_user_dict["id"]
    assert result.username == expected_user_dict["username"]
    assert result.first_name == expected_user_dict["first_name"]
    assert result.last_name == expected_user_dict["last_name"]
    assert result.created_at == arrow.get(2020, 4, 15)
    assert result.updated_at == arrow.get(2020, 4, 15)
