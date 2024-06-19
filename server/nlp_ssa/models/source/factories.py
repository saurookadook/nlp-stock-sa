import factory
from uuid import uuid4

from db import db_session
from models.mixins.factories import TimestampsMixinFactory
from models.source.db import SourceDB


class SourceFactory(TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SourceDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid4())
    data_type = None
    data_type_id = None
