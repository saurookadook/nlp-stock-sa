import arrow
import pytest
from unittest.mock import patch
from uuid import UUID, uuid4

from models.analysis_view import AnalysisViewFactory
from models.sentiment_analysis import SentimentAnalysisFactory
from models.user import User, UserFacade, UserFactory


@pytest.fixture
def mock_utcnow(monkeypatch):
    mock_utcnow_return = arrow.get(2024, 4, 19)
    # monkeypatch.setattr(arrow, "utcnow", lambda: mock_utcnow_return)
    return mock_utcnow_return


@pytest.fixture
def user_facade(mock_db_session):
    return UserFacade(db_session=mock_db_session)


def test_get_one_by_id(mock_db_session, user_facade):
    mock_user = UserFactory()
    mock_db_session.commit()

    result = user_facade.get_one_by_id(id=mock_user.id)

    assert result == User.model_validate(mock_user)


def test_get_one_by_id_no_result(user_facade):
    with pytest.raises(UserFacade.NoResultFound):
        user_facade.get_one_by_id(id="415c5a59-942b-4f08-acb5-2c16f2b37c9b")


def test_get_one_by_username(mock_db_session, user_facade):
    mock_user = UserFactory()
    mock_db_session.commit()

    result = user_facade.get_one_by_username(username=mock_user.username)

    assert result == User.model_validate(mock_user)


def test_get_one_by_username_no_result(user_facade):
    with pytest.raises(UserFacade.NoResultFound):
        user_facade.get_one_by_username(username="does-not-exist")


def test_get_analysis_views_by_quote_stock_symbol_singular_result(
    mock_db_session, user_facade
):
    mock_user = UserFactory()
    sa_1 = SentimentAnalysisFactory(
        source_group_id=UUID("0a35cf9d-44e7-4e74-bb35-55605f093ce5"),
        quote_stock_symbol="TSLA",
    )
    mock_analysis_view = AnalysisViewFactory(
        source_group_id=sa_1.source_group_id, user=mock_user
    )
    mock_db_session.commit()

    result = user_facade.get_analysis_views_by_quote_stock_symbol("TSLA")

    assert result == [mock_analysis_view]


def test_get_analysis_views_by_quote_stock_symbol_multiple_results(
    mock_db_session, user_facade
):

    assert False == "Implement me! :["


def test_get_analysis_views_by_quote_stock_symbol_no_results(
    mock_db_session, user_facade
):
    UserFactory()
    mock_db_session.commit()

    result = user_facade.get_analysis_views_by_quote_stock_symbol("TSLA")

    assert result == []


def test_create_or_update_new_user(user_facade, mock_utcnow):
    user_dict = {
        "id": uuid4(),
        "first_name": "Walter",
        "last_name": "White",
        "username": "iamheisenberg",
        "email": "best-meth-cook@yahoo.com",
    }

    with patch("models.user.facade.arrow.utcnow", return_value=mock_utcnow) as mock_now:
        result = user_facade.create_or_update(payload=user_dict)

        assert result.first_name == user_dict["first_name"]
        assert result.last_name == user_dict["last_name"]
        assert result.username == user_dict["username"]
        assert result.email == user_dict["email"]
        assert result.created_at == mock_now()
        assert result.updated_at == mock_now()
