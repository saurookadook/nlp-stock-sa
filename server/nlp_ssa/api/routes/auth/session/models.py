from typing import Optional

from constants import AuthProviderEnum, TokenTypeEnum
from utils.pydantic_helpers import BaseResponseModel


class SessionCookieConfig(BaseResponseModel):
    key: str
    value: str = ""
    max_age: int
    domain: str
    httponly: bool


class TokenData(BaseResponseModel):
    access_token: str
    expires_in: int
    refresh_token: Optional[str]
    refresh_token_expires_in: int
    token_type: TokenTypeEnum
    scope: Optional[str]


class UserSessionCacheDetails(BaseResponseModel):
    auth_provider: AuthProviderEnum
    cookie_config: SessionCookieConfig
    token_data: Optional[TokenData]
