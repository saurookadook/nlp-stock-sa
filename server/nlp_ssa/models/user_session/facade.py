import arrow
from sqlalchemy import and_, delete, literal_column, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from uuid import UUID

from constants import AuthProviderEnum
from models.user_session import UserSessionDB
from models.user_session.user_session import UserSession


class UserSessionFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, id: UUID):
        try:
            user_session = self.db_session.execute(
                select(UserSessionDB).where(UserSessionDB.id == id)
            ).scalar_one()
        except NoResultFound:
            raise UserSessionFacade.NoResultFound

        return UserSession.model_validate(user_session)

    def get_first_by_user_id_and_auth_provider(
        self, user_id: UUID, auth_provider: AuthProviderEnum
    ):
        user_session = (
            self.db_session.execute(
                select(UserSessionDB).where(
                    and_(
                        UserSessionDB.auth_provider == auth_provider,
                        UserSessionDB.user_id == user_id,
                    )
                )
            )
            .scalars()
            .first()
        )

        if not user_session:
            return None

        return UserSession.model_validate(user_session)

    def get_all_by_user_id(self, user_id: UUID):
        try:
            user_sessions = (
                self.db_session.execute(
                    select(UserSessionDB).where(
                        UserSessionDB.user_id == user_id,
                    )
                )
                .scalars()
                .all()
            )
        except NoResultFound:
            raise UserSessionFacade.NoResultFound

        return [UserSession.model_validate(us) for us in user_sessions]

    def create_or_update(self, *, payload: Dict) -> UserSession:
        pass

    def delete_one_by_id(self, id: UUID):
        pass
