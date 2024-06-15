from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from uuid import UUID

from db import Base
from models.mixins.db import TimestampsMixinDB, SourceAssociationDB


class SourceDB(TimestampsMixinDB, Base):
    __tablename__ = "sources"

    association_id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True),
        ForeignKey(SourceAssociationDB.id),
    )
    association: Mapped[SourceAssociationDB] = relationship(
        back_populates="data_source", uselist=False
    )
    data: AssociationProxy = association_proxy("association", "data")

    related_sentiment_analyses: Mapped[List["SentimentAnalysisDB"]] = relationship(
        back_populates="source"
    )
