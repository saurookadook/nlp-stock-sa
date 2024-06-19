import factory
from uuid import uuid4

from db import db_session
from models.mixins.factories import TimestampsMixinFactory
from models.user import UserDB
from utils.case_converters import convert_to_kebab_case


class UserFactory(TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid4())
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.LazyAttribute
    def username(self):
        return convert_to_kebab_case(f"{self.first_name}-{self.last_name}")

    @factory.LazyAttribute
    def email(self):
        return f"{self.first_name}-{self.last_name}@lolz.net".lower()
