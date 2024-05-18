import arrow
from sqlalchemy import literal_column, select
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

    def create_or_update(self, *, payload: Dict) -> Stock:
        insert_stmt = insert(StockDB).values(**payload)

        full_stmt = insert_stmt.on_conflict_do_update(
            constraint=StockDB.__table__.primary_key,
            set_={
                **payload,
                # "created_at": arrow.utcnow(),
                "updated_at": arrow.utcnow(),
            },
        ).returning(literal_column("*"))

        article_data = self.db_session.execute(full_stmt).fetchone()
        self.db_session.flush()

        return Stock.model_validate(article_data)
