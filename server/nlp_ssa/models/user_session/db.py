import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants.db_types import (
    AuthProviderEnum,
    AuthProviderEnumDB,
    TokenTypeEnum,
    TokenTypeEnumDB,
)
from db import Base
from models.mixins import TimestampsDB


class UserSessionDB(Base, TimestampsDB):
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    cache_key: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserDB"] = relationship(back_populates="user_sessions")
    access_token: Mapped[str] = mapped_column(nullable=False, unique=True)
    auth_provider: Mapped[AuthProviderEnum] = mapped_column(
        AuthProviderEnumDB, nullable=False, unique=False
    )
    expires_in: Mapped[int] = mapped_column(nullable=False, unique=False)
    # TODO: should this have some other validation? and/or encrypted somehow?
    refresh_token: Mapped[str] = mapped_column(nullable=True, unique=True)
    refresh_token_expires_in: Mapped[int] = mapped_column(nullable=True, unique=False)
    token_type: Mapped[TokenTypeEnum] = mapped_column(
        TokenTypeEnumDB, nullable=False, unique=False
    )
