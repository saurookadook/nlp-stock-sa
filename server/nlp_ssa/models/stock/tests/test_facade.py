import pytest
from sqlalchemy import select
from uuid import UUID

from models.stock import StockDB, StockFacade
from models.stock.stock import Stock
from models.stock.factories import StockFactory


@pytest.fixture
def stock_facade(mock_db_session):
    return StockFacade(db_session=mock_db_session)


def test_get_one_by_id(mock_db_session, stock_facade):
    mock_stock = StockFactory()
    mock_db_session.commit()

    result = stock_facade.get_one_by_id(id=mock_stock.id)

    assert result == Stock.model_validate(mock_stock)


def test_get_one_by_id_no_result(stock_facade):
    with pytest.raises(StockFacade.NoResultFound):
        stock_facade.get_one_by_id(id="415c5a59-942b-4f08-acb5-2c16f2b37c9b")


def test_get_one_by_quote_stock_symbol(mock_db_session, stock_facade):
    mock_stock = StockFactory()
    mock_db_session.commit()

    result = stock_facade.get_one_by_quote_stock_symbol(
        quote_stock_symbol=mock_stock.quote_stock_symbol
    )

    assert result == Stock.model_validate(mock_stock)


def test_get_one_by_quote_stock_symbol_no_result(stock_facade):
    with pytest.raises(StockFacade.NoResultFound):
        stock_facade.get_one_by_quote_stock_symbol(quote_stock_symbol="NOPE")


def test_create_or_update_new_stock(mock_db_session, stock_facade):
    stock_dict = {
        "id": UUID("5cabc780-62bb-406a-9f63-b97cf7f181b8"),
        "quote_stock_symbol": "NTDOF",
        "full_stock_symbol": "Nintendo",
    }

    result = stock_facade.create_or_update(payload=stock_dict)
    assert result.id == stock_dict["id"]
    assert result.quote_stock_symbol == stock_dict["quote_stock_symbol"]
    assert result.full_stock_symbol == stock_dict["full_stock_symbol"]

    mock_db_session.commit()

    expected = mock_db_session.execute(
        select(StockDB).where(
            StockDB.quote_stock_symbol == stock_dict["quote_stock_symbol"]
        )
    ).scalar_one()

    assert expected.id == stock_dict["id"]
    assert expected.quote_stock_symbol == stock_dict["quote_stock_symbol"]
    assert expected.full_stock_symbol == stock_dict["full_stock_symbol"]


def test_create_or_update_existing_stock(mock_db_session, stock_facade):
    mock_stock = StockFactory(
        id=UUID("d1bf5370-460b-40d5-90b0-47d711faea8e"),
        quote_stock_symbol="MEOW",
        full_stock_symbol="Meow Inc.",
    )
    mock_db_session.commit()

    stock_dict = {
        "id": mock_stock.id,
        "quote_stock_symbol": "NTDOF",
        "full_stock_symbol": "Nintendo",
    }

    result = stock_facade.create_or_update(payload=stock_dict)
    assert result.id == stock_dict["id"]
    assert result.quote_stock_symbol == stock_dict["quote_stock_symbol"]
    assert result.full_stock_symbol == stock_dict["full_stock_symbol"]

    mock_db_session.commit()

    expected = mock_db_session.execute(
        select(StockDB).where(
            StockDB.quote_stock_symbol == stock_dict["quote_stock_symbol"]
        )
    ).scalar_one()

    assert expected.id == stock_dict["id"]
    assert expected.quote_stock_symbol == stock_dict["quote_stock_symbol"]
    assert expected.full_stock_symbol == stock_dict["full_stock_symbol"]
