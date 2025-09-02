import factory
import secrets
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
    # TODO: set or generate username?
    cache_key = factory.LazyFunction(
        lambda: f"username_placeholder:{secrets.token_urlsafe(17)}"
    )
    access_token = factory.LazyFunction(lambda: "ghu_" + secrets.token_hex(18))
    auth_provider = AuthProviderEnum.GITHUB.value
    expires_in = EIGHT_HOURS_IN_SECONDS
    refresh_token = factory.LazyFunction(lambda: "ghr_" + secrets.token_hex(38))
    refresh_token_expires_in = SIX_MONTHS_IN_SECONDS
    token_type = TokenTypeEnum.BEARER.value

    @factory.post_generation
    def user(_self, create, extracted, **kwargs):
        if extracted is not None:
            _self.user_id = extracted.id
