import factory
from uuid import uuid4

from db import db_session
from models.analysis_view import AnalysisViewDB
from models.mixins import TimestampsMixinFactory
from models.user.factories import UserFactory


class AnalysisViewFactory(
    TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory
):
    class Meta:
        model = AnalysisViewDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid4())
    source_group_id = factory.LazyFunction(lambda: uuid4())
    # owner = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)
