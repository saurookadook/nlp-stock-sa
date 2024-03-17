import arrow
import factory
import uuid

from db import db_session
from models.sentiment_analysis import SentimentAnalysisDB, SentimentEnum


class SentimentAnalysisFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SentimentAnalysisDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    quote_stock_symbol = factory.Faker("stock_symbol")  # TODO: fix this lol
    sentiment = SentimentEnum.NEUTRAL.value
    score = factory.Transformer(
        factory.Faker("random_int", min=11, max=999), transform=lambda o: o / 10
    )
    source_group_id = factory.LazyFunction(lambda: uuid.uuid4())
    created_at = arrow.utcnow()
    updated_at = arrow.utcnow()

    @factory.LazyAttribute
    def email(self):
        return f"{self.first_name}-{self.last_name}@lolz.net"
