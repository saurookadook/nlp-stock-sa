import arrow
import factory
import uuid

from db import Session
from models.sentiment_analysis import SentimentAnalysisDB


class SentimentAnalysisFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SentimentAnalysisDB
        sqlalchemy_session = Session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    stock_symbol = factory.Faker("stock_symbol")  # TODO: fix this lol
    sentiment = "neutral"  # TODO: use enum instead
    source_group_id = factory.LazyFunction(lambda: uuid.uuid4())
    created_at = arrow.utcnow()
    updated_at = arrow.utcnow()

    @factory.LazyAttribute
    def email(self):
        return f"{self.first_name}-{self.last_name}@lolz.net"
