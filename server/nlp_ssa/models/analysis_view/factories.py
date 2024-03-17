import arrow
import factory
import uuid

from db import db_session
from models.sentiment_analysis import AnalysisViewDB
from models.user import UserFactory


class AnalysisViewFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AnalysisViewDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    source_group_id = factory.LazyFunction(lambda: uuid.uuid4())
    # owner = factory.SubFactory(UserFactory)
    owner_id = factory.LazyFunction(lambda: uuid.uuid4())
    user_id = factory.LazyFunction(lambda: uuid.uuid4())
    created_at = arrow.utcnow()
    updated_at = arrow.utcnow()
