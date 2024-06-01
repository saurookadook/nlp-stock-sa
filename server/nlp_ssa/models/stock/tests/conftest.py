import pytest

from models.stock import StockFacade


@pytest.fixture
def stock_facade(mock_db_session):
    return StockFacade(db_session=mock_db_session)
