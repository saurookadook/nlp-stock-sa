import arrow
from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

from db import Base, ArrowDate


class UserDB(Base):
    __tablename__ = "users"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, nullable=False)
    username = Column(String(length=255), nullable=False, unique=True)
    # TODO: need to encrypt this :)
    # password = Column()
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    created_at = Column(ArrowDate(), nullable=False, server_default=func.now())
    updated_at = Column(
        ArrowDate(), nullable=False, server_default=func.now(), onupdate=arrow.utcnow
    )
