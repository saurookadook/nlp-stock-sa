import factory
import uuid

from db import db_session
from models.article_data import ArticleDataDB
from models.mixins import TimestampsMixinFactory


class ArticleDataFactory(
    TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory
):
    class Meta:
        model = ArticleDataDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    quote_stock_symbol = factory.Transformer(
        factory.Faker("random_letters", length=6),
        transform=lambda o: "".join(o).upper(),
    )
    source_group_id = factory.LazyFunction(lambda: uuid.uuid4())
    source_url = factory.Faker("url")
    raw_content = factory.Faker("text", max_nb_chars=5000)
    # TODO: make this clean text like in the scrapers
    sentence_tokens = factory.LazyAttribute(lambda ad: ad.raw_content)
