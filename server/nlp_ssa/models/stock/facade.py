from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from models.stock import Stock, StockDB


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
