import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from constants.db_types import (
    AuthProviderEnum,
    AuthProviderEnumDB,
    TokenTypeEnum,
    TokenTypeEnumDB,
)
from db import ArrowDate, Base
from models.mixins import TimestampsDB


class UserSessionDB(Base, TimestampsDB):
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserDB"] = relationship(back_populates="user_sessions")
    auth_provider: Mapped[AuthProviderEnum] = mapped_column(
        AuthProviderEnumDB, nullable=False, unique=False
    )
    expires_in = Column(ArrowDate(), nullable=False, unique=False)
    # TODO: should this have some other validation? and/or encrypted somehow?
    refresh_token: Mapped[str] = mapped_column(nullable=True, unique=True)
    refresh_token_expres_in = Column(ArrowDate(), nullable=True, unique=False)
    token_type: Mapped[TokenTypeEnum] = mapped_column(
        TokenTypeEnumDB, nullable=False, unique=False
    )
