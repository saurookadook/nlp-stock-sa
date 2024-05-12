import arrow
import pytest
from sqlalchemy import select, and_
from unittest import mock
from uuid import UUID

from models.stock import StockDB
from models.stock.factories import StockFactory


@pytest.fixture(autouse=True)
def mock_utcnow():
    mock.patch("arrow.utcnow", return_value=arrow.get(2024, 3, 11))
    return mock_utcnow


@pytest.fixture
def expected_stock_dict():
    return dict(
        id=UUID("4c26429c-c8e8-4fc6-9b39-357d3e5e7dd6"),
        quote_stock_symbol="CATZ",
        full_stock_symbol="Caring About The Zebraz, LLC",
    )


def test_stock_db(mock_db_session, expected_stock_dict):
    stock = StockFactory(**expected_stock_dict)
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(StockDB).where(
            and_(
                StockDB.id == stock.id,
                StockDB.quote_stock_symbol == stock.quote_stock_symbol,
            )
        )
    ).scalar_one()

    assert result.id == expected_stock_dict["id"]
    assert result.quote_stock_symbol == expected_stock_dict["quote_stock_symbol"]
    assert result.full_stock_symbol == expected_stock_dict["full_stock_symbol"]
    assert result.created_at == arrow.get(2020, 4, 15)
    assert result.updated_at == arrow.get(2020, 4, 15)
