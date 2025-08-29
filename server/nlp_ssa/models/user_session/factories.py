import factory
from uuid import uuid4

from constants import (
    AuthProviderEnum,
    TokenTypeEnum,
    EIGHT_HOURS_IN_SECONDS,
    SIX_MONTHS_IN_SECONDS,
)
from db import db_session
from models.mixins.factories import TimestampsMixinFactory
from models.user_session import UserSessionDB


class UserSessionFactory(
    TimestampsMixinFactory, factory.alchemy.SQLAlchemyModelFactory
):
    class Meta:
        model = UserSessionDB
        sqlalchemy_session = db_session

    id = factory.LazyFunction(lambda: uuid4())
    access_token = factory.Transformer(
        factory.Faker("sha256", lenght=36),
        transform=lambda o: o if "ghu_" in o else "ghu_" + o,
    )
    auth_provider = AuthProviderEnum.GITHUB.value
    expires_in = EIGHT_HOURS_IN_SECONDS
    refresh_token = factory.Transformer(
        factory.Faker("sha256", lenght=76),
        transform=lambda o: o if "ghr_" in o else "ghr_" + o,
    )
    refresh_token_expires_in = SIX_MONTHS_IN_SECONDS
    token_type = TokenTypeEnum.BEARER.value

    @factory.post_generation
    def user(_self, create, extracted, **kwargs):
        if extracted is not None:
            _self.user_id = extracted.id
