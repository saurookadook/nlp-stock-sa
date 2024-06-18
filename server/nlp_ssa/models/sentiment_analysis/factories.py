import factory
from uuid import uuid4

from constants import SentimentEnum
from db import db_session
from models.mixins.factories import TimestampsMixinFactory
from models.sentiment_analysis import SentimentAnalysisDB


class SentimentAnalysisFactory(
    TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory
):
    class Meta:
        model = SentimentAnalysisDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid4())
    quote_stock_symbol = factory.Transformer(
        factory.Faker("random_letters", length=6),
        transform=lambda o: "".join(o).upper(),
    )
    source_group_id = factory.LazyFunction(lambda: uuid4())
    source_id = None
    source = None
    output = {"compound": 0, "neg": 0, "neu": 0, "pos": 0}
    # TODO: make sentiment and score lazy attributes based on output
    sentiment = SentimentEnum.NEUTRAL.value
    score = factory.Transformer(
        factory.Faker("random_int", min=11, max=999),
        transform=lambda o: o / 10 if type(o) is int else o,
    )

    # TODO: maybe sometime...?
    # @factory.post_generation
    # def set_source(_self, create, extracted, **kwargs):
    #     from models.source.factories import SourceFactory

    #     source = SourceFactory()
    #     _self.source_id = source.id
    #     _self.source = source
