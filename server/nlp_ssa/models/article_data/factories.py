import factory
from uuid import uuid4

from db import db_session
from models.article_data import ArticleDataDB
from models.mixins.factories import (
    OwnedByPolymorphicSourceFactory,
    TimestampsMixinFactory,
)
from utils.testing_mocks import get_mock_utcnow


class ArticleDataFactory(
    OwnedByPolymorphicSourceFactory,
    TimestampsMixinFactory,
    factory.alchemy.SQLAlchemyModelFactory,
):
    class Meta:
        model = ArticleDataDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid4())
    last_updated_date = factory.LazyFunction(lambda: get_mock_utcnow())
    published_date = factory.LazyFunction(lambda: get_mock_utcnow().shift(months=-6))
    quote_stock_symbol = factory.Transformer(
        factory.Faker("random_letters", length=6),
        transform=lambda o: "".join(o).upper(),
    )
    raw_content = factory.Faker("text", max_nb_chars=5000)
    # TODO: make this clean text like in the scrapers
    sentence_tokens = factory.LazyAttribute(lambda ad: ad.raw_content)
    source_group_id = factory.LazyFunction(lambda: uuid4())
    source_url = factory.Faker("url")
