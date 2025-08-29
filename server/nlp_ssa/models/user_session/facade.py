import arrow
from sqlalchemy import and_, literal_column, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from uuid import UUID

from models.user_session import UserSessionDB
from models.user_session.user_session import UserSession


class UserSessionFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session
