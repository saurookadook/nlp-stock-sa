import factory

from utils.testing_mocks import get_mock_utcnow


class TimestampsMixinFactory(factory.alchemy.SQLAlchemyModelFactory):
    created_at = get_mock_utcnow()
    updated_at = get_mock_utcnow()
