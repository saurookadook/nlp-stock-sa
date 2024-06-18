import arrow
from sqlalchemy import Column, event, and_
from sqlalchemy.orm import backref, foreign, relationship, remote
from sqlalchemy.sql import func

from db import ArrowDate


class TimestampsDB(object):
    created_at = Column(ArrowDate(), nullable=False, server_default=func.now())
    updated_at = Column(
        ArrowDate(), nullable=False, server_default=func.now(), onupdate=arrow.utcnow
    )


class OwnedByPolymorphicSourceDB:
    """Mixin for programatically setting `polymorphic_source` property on inherited models."""

    __table_args__ = {"extend_existing": True}


@event.listens_for(OwnedByPolymorphicSourceDB, "mapper_configured", propagate=True)
def setup_listener(mapper, class_ref):
    from constants import SourceDiscriminatorEnum
    from models.source.db import SourceDB

    ModelName = class_ref.__name__
    data_type = SourceDiscriminatorEnum[ModelName]

    class_ref.polymorphic_source = relationship(
        SourceDB,
        primaryjoin=and_(
            class_ref.id == foreign(remote(SourceDB.data_type_id)),
            SourceDB.data_type == data_type,
        ),
        backref=backref(
            "data",
            primaryjoin=and_(
                remote(class_ref.id) == foreign(SourceDB.data_type_id),
                SourceDB.data_type == data_type,
            ),
        ),
        uselist=False,
    )

    @event.listens_for(class_ref.polymorphic_source, "set")
    def set_source(target: class_ref, value: SourceDB, old_value: SourceDB, initiator):
        ModelName = target.__class__.__name__
        value.data_type = SourceDiscriminatorEnum[ModelName]
        value.data_type_id = target.id
