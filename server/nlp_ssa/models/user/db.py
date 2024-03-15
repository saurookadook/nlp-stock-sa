import arrow
from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql

from db import Base
from models.mixins import TimestampsMixin


class UserDB(Base, TimestampsMixin):
    __tablename__ = "users"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, nullable=False)
    username = Column(String(length=255), nullable=False, unique=True)
    # email = Column(String(length=255), nullable=False, unique=True)
    # TODO: need to encrypt this :)
    # password = Column()
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
