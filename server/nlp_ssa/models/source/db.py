from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from db import Base
from models.mixins.db import TimestampsMixinDB


class SourceDB(Base, TimestampsMixinDB):
    __tablename__ = "source"

    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    association_id: Mapped[UUID] = mapped_column(
        ForeignKey("source_association.id"), nullable=True
    )
    association: Mapped["SourceAssociationDB"] = relationship(
        "SourceAssociationDB", backref="source", single_parent=True
    )
    data: AssociationProxy = association_proxy("association", "data")
