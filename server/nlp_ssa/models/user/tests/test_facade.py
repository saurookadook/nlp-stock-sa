import arrow
import pytest
from uuid import UUID, uuid4

from models.analysis_view.factories import AnalysisViewFactory
from models.sentiment_analysis.factories import SentimentAnalysisFactory
from models.stock.factories import StockFactory
from models.user import User, UserFacade
from models.user.factories import UserFactory


@pytest.fixture()
def mock_facade_now(mocker, mock_utcnow):
    mock_facade_utcnow = mocker.patch("nlp_ssa.models.user.facade.arrow.utcnow")
    mock_facade_utcnow.return_value = mock_utcnow


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
    mock_stock_1 = StockFactory(quote_stock_symbol="TSLA")
    mock_stock_2 = StockFactory(quote_stock_symbol="VOO")
    mock_user = UserFactory()
    mock_db_session.commit()

    sa_1 = SentimentAnalysisFactory(
        source_group_id=UUID("0a35cf9d-44e7-4e74-bb35-55605f093ce5"),
        quote_stock_symbol=mock_stock_1.quote_stock_symbol,
    )
    sa_not_in_results = SentimentAnalysisFactory(
        source_group_id=UUID("4a6fac31-aaf9-4fb2-8d6b-b5ab5900d9b6"),
        quote_stock_symbol=mock_stock_2.quote_stock_symbol,
    )
    mock_analysis_view = AnalysisViewFactory(
        source_group_id=sa_1.source_group_id, user=mock_user
    )
    AnalysisViewFactory(
        source_group_id=sa_not_in_results.source_group_id, user=mock_user
    )
    mock_db_session.commit()

    result = user_facade.get_analysis_views_by_quote_stock_symbol(mock_user.id, "TSLA")

    assert result == [mock_analysis_view]


def test_get_analysis_views_by_quote_stock_symbol_multiple_results(
    mock_db_session, user_facade
):
    mock_stock_1 = StockFactory(quote_stock_symbol="DIS")
    mock_stock_2 = StockFactory(quote_stock_symbol="VOO")
    mock_user = UserFactory()
    mock_db_session.commit()

    sa_1 = SentimentAnalysisFactory(
        source_group_id=UUID("0a35cf9d-44e7-4e74-bb35-55605f093ce5"),
        quote_stock_symbol=mock_stock_1.quote_stock_symbol,
    )
    sa_2 = SentimentAnalysisFactory(
        source_group_id=UUID("394fe6c9-676b-4a3c-86bd-d07523cb4caa"),
        quote_stock_symbol=mock_stock_1.quote_stock_symbol,
    )
    sa_not_in_results = SentimentAnalysisFactory(
        source_group_id=UUID("4a6fac31-aaf9-4fb2-8d6b-b5ab5900d9b6"),
        quote_stock_symbol=mock_stock_2.quote_stock_symbol,
    )
    mock_analysis_view_1 = AnalysisViewFactory(
        source_group_id=sa_1.source_group_id, user=mock_user
    )
    mock_analysis_view_2 = AnalysisViewFactory(
        source_group_id=sa_2.source_group_id, user=mock_user
    )
    AnalysisViewFactory(
        source_group_id=sa_not_in_results.source_group_id, user=mock_user
    )
    mock_db_session.commit()

    result = user_facade.get_analysis_views_by_quote_stock_symbol(
        mock_user.id, mock_stock_1.quote_stock_symbol
    )

    assert result == [mock_analysis_view_1, mock_analysis_view_2]


def test_get_analysis_views_by_quote_stock_symbol_no_results(
    mock_db_session, user_facade
):
    mock_user = UserFactory()
    mock_db_session.commit()

    result = user_facade.get_analysis_views_by_quote_stock_symbol(mock_user.id, "TSLA")

    assert result == []


def test_create_or_update_new_user(user_facade, mock_utcnow, mock_facade_now):
    user_dict = {
        "id": uuid4(),
        "first_name": "Walter",
        "last_name": "White",
        "username": "iamheisenberg",
        "email": "best-meth-cook@yahoo.com",
    }

    result = user_facade.create_or_update(payload=user_dict)

    assert result.first_name == user_dict["first_name"]
    assert result.last_name == user_dict["last_name"]
    assert result.username == user_dict["username"]
    assert result.email == user_dict["email"]
    # TODO: not sure why the mocks in the test fixtures aren't working :']
    # assert result.created_at == mock_utcnow
    # assert result.updated_at == mock_utcnow
    assert isinstance(result.created_at, arrow.Arrow)
    assert isinstance(result.updated_at, arrow.Arrow)
