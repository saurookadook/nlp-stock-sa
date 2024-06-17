import factory

from constants import SourceDiscriminatorEnum
from utils.testing_mocks import get_mock_utcnow


class OwnedByPolymorphicSourceFactory(factory.alchemy.SQLAlchemyModelFactory):

    @factory.post_generation
    def set_polymorphic_source(_self, create, extracted, **kwargs):
        from models.source.factories import SourceFactory

        ModelName = _self.__class__.__name__
        source = SourceFactory(
            data_type=SourceDiscriminatorEnum[ModelName],
            data_type_id=_self.id,
        )
        _self.polymorphic_source = source


class TimestampsMixinFactory(factory.alchemy.SQLAlchemyModelFactory):
    created_at = get_mock_utcnow()
    updated_at = get_mock_utcnow()
