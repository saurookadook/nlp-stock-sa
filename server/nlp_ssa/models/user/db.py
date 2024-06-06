import uuid
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from db import Base
from models.mixins import TimestampsMixinDB


class UserDB(Base, TimestampsMixinDB):
    from models.analysis_view import AnalysisViewDB

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(length=255), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    # TODO: need to encrypt this :)
    # password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=255), nullable=True)

    #####
    # TODO: configure polymorphic relationship at some point (aka "generic association")
    # https://docs.sqlalchemy.org/en/20/orm/examples.html#module-examples.generic_associations
    #####
    analysis_views: Mapped[List[AnalysisViewDB]] = relationship(back_populates="user")
