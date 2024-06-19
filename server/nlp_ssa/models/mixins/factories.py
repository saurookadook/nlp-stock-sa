import factory

from constants import SourceDiscriminatorEnum
from utils.testing_mocks import get_mock_utcnow


class OwnedByPolymorphicSourceFactory(factory.alchemy.SQLAlchemyModelFactory):
    # polymorphic_source = factory.SubFactory("models.source.factories.SourceFactory")

    @factory.post_generation
    def set_polymorphic_source(_self, create, extracted, **kwargs):
        # TODO: feels like there should be a better way to do this...

        if _self.polymorphic_source is not None:
            return
        elif create and _self.polymorphic_source is None:
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
