import factory
import uuid

from db import db_session
from models.analysis_view import AnalysisViewDB
from models.mixins import TimestampsMixinFactory
from models.user import UserFactory


class AnalysisViewFactory(
    TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory
):
    class Meta:
        model = AnalysisViewDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    source_group_id = factory.LazyFunction(lambda: uuid.uuid4())
    # owner = factory.SubFactory(UserFactory)
    owner_id = factory.LazyFunction(lambda: uuid.uuid4())
    user_id = factory.LazyFunction(lambda: uuid.uuid4())
