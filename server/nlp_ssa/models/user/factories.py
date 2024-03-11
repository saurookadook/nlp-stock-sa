import arrow
import factory
import uuid

from db import db_session
from models.user import UserDB


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid.uuid4())
    username = factory.Faker("username")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    created_at = arrow.get(2020, 4, 15)
    updated_at = arrow.get(2020, 4, 15)

    # @factory.LazyAttribute
    # def email(self):
    #     return f"{self.first_name}-{self.last_name}@lolz.net"
