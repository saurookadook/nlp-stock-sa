from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from uuid import UUID

# from constants import SourceDiscriminatorEnum
# from constants.db_types import SourceDiscriminatorEnum, SourceDiscriminatorEnumDB
from db import Base
from models.mixins import TimestampsMixinDB


# SourceDiscriminatorEnumDB = postgresql.ENUM(
#     SourceDiscriminatorEnum,
#     values_callable=lambda e: [x.value for x in e],
#     name=SourceDiscriminatorEnum.db_type_name(),
#     metadata=Base.metadata,
# )


# class SourceAssociationDB(Base):
#     """Associates a Source object with a particular type of data."""

#     __tablename__ = "source_association"

#     id: Mapped[UUID] = mapped_column(
#         postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
#     )
#     discriminator: Mapped[SourceDiscriminatorEnum] = mapped_column(
#         SourceDiscriminatorEnumDB,
#         server_default=SourceDiscriminatorEnum.ARTICLE_DATA.value,
#         default=SourceDiscriminatorEnum.ARTICLE_DATA,
#         nullable=False,
#     )

#     __mapper_args__ = {"polymorphic_on": discriminator}


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
