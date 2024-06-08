from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from uuid import UUID

from constants import SourceDiscriminatorEnum
from db import Base
from models.mixins import TimestampsMixinDB


SOURCE_DISCRIMINATOR_ENUM = postgresql.ENUM(
    SourceDiscriminatorEnum,
    values_callable=lambda e: [x.value for x in e],
    name="source_discriminators",
    metadata=Base.metadata,
)


class SourceAssociationDB(Base):
    """Associates a Source object with a particular type of data."""

    __tablename__ = "source_association"

    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    discriminator: Mapped[SourceDiscriminatorEnum] = mapped_column(
        SOURCE_DISCRIMINATOR_ENUM,
        default=SourceDiscriminatorEnum.ARTICLE_DATA,
        server_default=SourceDiscriminatorEnum.ARTICLE_DATA.value,
        nullable=False,
    )

    __mapper_args__ = {"polymorphic_on": discriminator}


class SourceDB(Base, TimestampsMixinDB):
    __tablename__ = "source"

    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    association_id: Mapped[UUID] = mapped_column(
        ForeignKey("source_association.id"), nullable=False
    )
    association: Mapped["SourceAssociationDB"] = relationship(
        "SourceAssociationDB", backref="source"
    )
    data: AssociationProxy = association_proxy("association", "data")


class PolymorphicSourceDB:
    """PolymorphicSourceDB mixin, creates a relationship to
    the source_association table for each data.

    """

    @declared_attr
    def source_association_id(cls):
        return mapped_column(
            postgresql.UUID(as_uuid=True),
            ForeignKey(f"{SourceAssociationDB.__tablename__}.id"),
        )

    @declared_attr
    def source_association(cls):
        assoc_cls = type(
            f"{cls.__name__}SourceAssociationDB",
            (SourceAssociationDB,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": cls.__name__.lower()},
            ),
        )

        cls.source = association_proxy(
            "source_association",
            "source",
            creator=lambda sourcees: assoc_cls(sourcees=sourcees),
        )
        return relationship(assoc_cls, back_populates="data", uselist=False)
