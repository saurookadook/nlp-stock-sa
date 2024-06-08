import factory
from uuid import uuid4

from db import db_session

# from models.article_data import ArticleDataDB
from models.mixins import TimestampsMixinFactory
from models.source.db import SourceDB


class SourceFactory(TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        mode = SourceDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid4())
    # TODO: fairly certain there should be more setup for the relationship...
    association_id = factory.LazyFunction(lambda: uuid4())
