import uuid
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from db import Base
from models.mixins import TimestampsMixin


class UserDB(Base, TimestampsMixin):
    from models.analysis_view.db import AnalysisViewDB

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

    analysis_views: Mapped[List["AnalysisViewDB"]] = relationship(
        back_populates="owner"
    )
