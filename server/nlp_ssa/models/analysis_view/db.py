from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from db import Base
from models.mixins import TimestampsMixinDB


class AnalysisViewDB(TimestampsMixinDB, Base):
    __tablename__ = "analysis_views"

    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    source_group_id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), nullable=False
    )
    #####
    # TODO: configure polymorphic relationship at some point (aka "generic association")
    # https://docs.sqlalchemy.org/en/20/orm/examples.html#module-examples.generic_associations
    #####
    # owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    # owner: Mapped["UserDB"] = relationship(back_populates="analysis_views")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["UserDB"] = relationship(  # noqa: F821
        "UserDB", back_populates="analysis_views"
    )
