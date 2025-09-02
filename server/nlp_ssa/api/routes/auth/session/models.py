from typing import Optional
from uuid import UUID

from constants import AuthProviderEnum, TokenTypeEnum
from utils.pydantic_helpers import BaseResponseModel, SerializerArrowType


class SessionCookieConfig(BaseResponseModel):
    key: str
    value: str = ""
    max_age: int
    domain: str
    httponly: bool = True


class TokenData(BaseResponseModel):
    access_token: str
    expires_in: int
    refresh_token: Optional[str]
    refresh_token_expires_in: int
    token_type: TokenTypeEnum
    scope: Optional[str] = ""


class UserSessionCacheDetails(BaseResponseModel):
    auth_provider: AuthProviderEnum = AuthProviderEnum.GITHUB
    cookie_config: SessionCookieConfig
    token_data: Optional[TokenData]


class UserSessionCacheValue(BaseResponseModel):
    auth_provider: AuthProviderEnum = AuthProviderEnum.GITHUB
    cookie_config: SessionCookieConfig
    expires_at: SerializerArrowType
    user_session_id: UUID
