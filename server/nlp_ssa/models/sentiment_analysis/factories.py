import factory
import uuid

from db import db_session
from models.mixins import TimestampsMixinFactory
from models.sentiment_analysis import SentimentAnalysisDB, SentimentEnum


class SentimentAnalysisFactory(
    TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory
):
    class Meta:
        model = SentimentAnalysisDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    quote_stock_symbol = factory.Transformer(
        factory.Faker("random_letters", length=6),
        transform=lambda o: "".join(o).upper(),
    )
    sentiment = SentimentEnum.NEUTRAL.value
    score = factory.Transformer(
        factory.Faker("random_int", min=11, max=999), transform=lambda o: o / 10
    )
    source_group_id = factory.LazyFunction(lambda: uuid.uuid4())
