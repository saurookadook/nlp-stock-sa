from __future__ import annotations
from pydantic import Field
from typing import Annotated
from uuid import UUID

from constants import AuthProviderEnum, TokenTypeEnum
from models.mixins import TimestampsMixin
from models.user.user import User
from utils.pydantic_helpers import BaseAppModel


class UserSession(BaseAppModel, TimestampsMixin):
    id: UUID
    cache_key: str
    user_id: Annotated[UUID, Field()]
    user: Annotated[User, Field()]
    access_token: str
    auth_provider: AuthProviderEnum
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    token_type: TokenTypeEnum
