import arrow
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import UUID

from constants.db_types import SourceDiscriminatorEnum, SourceDiscriminatorEnumDB
from db import ArrowDate, Base

# from models.source.db import SourceAssociationDB


class TimestampsMixinDB(object):
    created_at = Column(ArrowDate(), nullable=False, server_default=func.now())
    updated_at = Column(
        ArrowDate(), nullable=False, server_default=func.now(), onupdate=arrow.utcnow
    )


class SourceAssociationDB(Base):
    """Associates a Source object with a particular type of data."""

    __tablename__ = "source_association"

    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    discriminator: Mapped[SourceDiscriminatorEnum] = mapped_column(
        SourceDiscriminatorEnumDB,
        server_default=SourceDiscriminatorEnum.ARTICLE_DATA.value,
        default=SourceDiscriminatorEnum.ARTICLE_DATA,
        nullable=False,
    )

    __mapper_args__ = {"polymorphic_on": discriminator}


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
        ModelName = cls.__name__

        assoc_cls = type(
            f"{ModelName}SourceAssociationDB",
            (SourceAssociationDB,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": ModelName},
                # source=relationship(
                #     ModelName,
                #     back_populates="source_association",
                #     uselist=False
                # )
            ),
        )

        cls.source = association_proxy(
            "source_association",
            "source",
            creator=lambda source: assoc_cls(source=source),
        )
        return relationship(
            assoc_cls,
            backref=backref("data", uselist=False),
            # back_populates="data",
            # uselist=False
        )
