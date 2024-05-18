import arrow
from sqlalchemy import literal_column, or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from models.stock import StockDB
from models.stock.stock import Stock


class StockFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, id):
        try:
            stock = self.db_session.execute(
                select(StockDB).where(StockDB.id == id)
            ).scalar_one()
        except NoResultFound:
            raise StockFacade.NoResultFound

        return Stock.model_validate(stock)

    def get_one_by_quote_stock_symbol(self, quote_stock_symbol):
        try:
            stock = self.db_session.execute(
                select(StockDB).where(StockDB.quote_stock_symbol == quote_stock_symbol)
            ).scalar_one()
        except NoResultFound:
            raise StockFacade.NoResultFound

        return Stock.model_validate(stock)

    def create_or_update(self, *, payload: Dict) -> Stock:
        maybe_one = self._find_one_if_exists(
            id=payload.get("id"), quote_stock_symbol=payload.get("quote_stock_symbol")
        )
        if maybe_one:
            return self.update(payload=payload)

        insert_stmt = insert(StockDB).values(**payload)

        full_stmt = insert_stmt.on_conflict_do_update(
            constraint=StockDB.__table__.primary_key,
            set_={
                **payload,
                # "created_at": arrow.utcnow(),
                "updated_at": arrow.utcnow(),
            },
        ).returning(literal_column("*"))

        stock = self.db_session.execute(full_stmt).fetchone()
        self.db_session.flush()

        return Stock.model_validate(stock)

    def update(self, *, payload: Dict) -> Stock:
        update_stmt = (
            update(StockDB)
            .where(
                or_(
                    StockDB.id == payload.get("id"),
                    StockDB.quote_stock_symbol == payload.get("quote_stock_symbol"),
                )
            )
            .values(**payload)
        ).returning(literal_column("*"))

        updated_record = self.db_session.execute(update_stmt).fetchone()
        self.db_session.flush()

        return Stock.model_validate(updated_record)

    def _find_one_if_exists(self, *, id, quote_stock_symbol):
        try:
            return self.get_one_by_id(id)
        except StockFacade.NoResultFound:
            pass

        try:
            return self.get_one_by_quote_stock_symbol(quote_stock_symbol)
        except StockFacade.NoResultFound:
            pass

        return None
