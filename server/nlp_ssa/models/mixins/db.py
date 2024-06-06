import arrow
from sqlalchemy import Column
from sqlalchemy.sql import func

from db import ArrowDate


class TimestampsMixinDB(object):
    created_at = Column(ArrowDate(), nullable=False, server_default=func.now())
    updated_at = Column(
        ArrowDate(), nullable=False, server_default=func.now(), onupdate=arrow.utcnow
    )
