import factory
import uuid

from db import db_session
from models.mixins import TimestampsMixinFactory
from models.stock import StockDB


class StockFactory(TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = StockDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    quote_stock_symbol = factory.Transformer(
        factory.Faker("random_letters", length=6),
        transform=lambda o: "".join(o).upper(),
    )
    full_stock_symbol = factory.Faker("company")
