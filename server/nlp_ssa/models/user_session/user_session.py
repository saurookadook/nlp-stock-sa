from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from uuid import UUID

from constants import AuthProviderEnum, TokenTypeEnum
from models.mixins import TimestampsMixin
from models.user.user import User


class UserSession(BaseModel, TimestampsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: Annotated[UUID, Field()]
    user: Annotated[User, Field()]
    access_token: str
    auth_provider: AuthProviderEnum
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    token_type: TokenTypeEnum
