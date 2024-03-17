import pytest

from models.stock import StockFacade, StockFactory


@pytest.fixture
def stock_facade(mock_db_session):
    return StockFacade(db_session=mock_db_session)


def test_get_one_by_id(mock_db_session, stock_facade):
    mock_stock = StockFactory()
    mock_db_session.commit()

    result = stock_facade.get_one_by_id(id=mock_stock.id)

    assert result == mock_stock


def test_get_one_by_id_no_result(stock_facade):
    with pytest.raises(StockFacade.NoResultFound):
        stock_facade.get_one_by_id(id="415c5a59-942b-4f08-acb5-2c16f2b37c9b")
