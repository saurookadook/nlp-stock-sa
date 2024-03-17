import arrow
import factory


class TimestampsMixinFactory(factory.alchemy.SQLAlchemyModelFactory):
    created_at = arrow.get(2020, 4, 15)
    updated_at = arrow.get(2020, 4, 15)
