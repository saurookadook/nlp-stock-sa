import arrow
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from constants.db_types import SourceDiscriminatorEnum, SourceDiscriminatorEnumDB
from db import ArrowDate, Base


class TimestampsMixinDB(object):
    created_at = Column(ArrowDate(), nullable=False, server_default=func.now())
    updated_at = Column(
        ArrowDate(), nullable=False, server_default=func.now(), onupdate=arrow.utcnow
    )


class SourceAssociationDB(Base):
    """Associates a Source object with a particular type of data."""

    __tablename__ = "source_association"

    discriminator: Mapped[SourceDiscriminatorEnum] = mapped_column(
        SourceDiscriminatorEnumDB,
        server_default=SourceDiscriminatorEnum.get_default_value(),
        default=SourceDiscriminatorEnum.get_default_value(),
        nullable=False,
    )

    data_source: Mapped["SourceDB"] = relationship(
        "SourceDB", back_populates="association", uselist=False
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
            default=uuid4(),
        )

    @declared_attr
    def source_association(cls):
        ModelName = cls.__name__
        discriminator = SourceDiscriminatorEnum[ModelName]

        assoc_cls = type(
            f"{ModelName}SourceAssociationDB",
            (SourceAssociationDB,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": discriminator},
                data=relationship(
                    ModelName, back_populates="source_association", uselist=False
                ),
            ),
        )

        cls.data_source = association_proxy(
            "source_association",
            "data_source",
            creator=lambda data_source: assoc_cls(data_source=data_source),
        )
        return relationship(assoc_cls)


# @event.listens_for(PolymorphicSourceDB, "mapper_configured", propagate=True)
# def setup_listener(mapper, class_):
#     from models.source.db import SourceDB

#     ModelName = class_.__name__

#     class_.source = relationship(
#         SourceDB,
#         primaryjoin=and_(
#             class_.id == foreign(remote(SourceDB.association_id)),
#             SourceDB.discriminator == ModelName,
#         ),
#         # backref=backref(
#         #     f"parent_{ModelName}",
#         #     primaryjoin=remote(class_.id) == foreign(SourceDB.parent_id),
#         # ),
#     )

#     @event.listens_for(class_.source, "set")
#     def assign_source(target, value, initiator):
#         value.discriminator = ModelName
