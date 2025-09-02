import arrow
from sqlalchemy import and_, delete, literal_column, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, List
from uuid import UUID

from constants import AuthProviderEnum
from models.user_session import UserSessionDB
from models.user_session.user_session import UserSession


class UserSessionFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session: scoped_session[Session]):
        self.db_session = db_session

    def get_one_by_id(self, id: UUID | str) -> UserSession:
        try:
            user_session = self.db_session.execute(
                select(UserSessionDB).where(UserSessionDB.id == id)
            ).scalar_one()
        except NoResultFound:
            raise UserSessionFacade.NoResultFound

        return UserSession.model_validate(user_session)

    def get_one_by_cache_key(self, cache_key: str) -> UserSession:
        try:
            user_session = self.db_session.execute(
                select(UserSessionDB).where(UserSessionDB.cache_key == cache_key)
            ).scalar_one()
        except NoResultFound:
            raise UserSessionFacade.NoResultFound

        return UserSession.model_validate(user_session)

    def get_first_by_user_id_and_auth_provider(
        self, user_id: UUID | str, auth_provider: AuthProviderEnum
    ) -> UserSession | None:
        try:
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
        except Exception as e:
            raise e

        if not user_session:
            return None

        return UserSession.model_validate(user_session)

    def get_all_by_user_id(self, user_id: UUID | str) -> List[UserSession]:
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
        except Exception as e:
            raise e

        return [UserSession.model_validate(us) for us in user_sessions]

    def create_or_update(self, *, payload: Dict) -> UserSession:
        maybe_one = self._one_exists(payload)
        if maybe_one:
            return self.update(payload=payload)

        insert_stmt = insert(UserSessionDB).values(**payload)

        full_stmt = insert_stmt.on_conflict_do_update(
            constraint=UserSessionDB.__table__.primary_key,
            set_={
                **payload,
                "updated_at": arrow.utcnow(),
            },
        ).returning(UserSessionDB)

        user_session = self.db_session.execute(full_stmt).scalar_one()
        self.db_session.flush()

        return UserSession.model_validate(user_session)

    def update(self, payload: Dict) -> UserSession:
        update_stmt = (
            update(UserSessionDB)
            .where(UserSessionDB.id == payload.get("id"))
            .values(**payload)
            .returning(UserSessionDB)
        )

        updated_record = self.db_session.execute(update_stmt).scalar_one()
        self.db_session.flush()

        return UserSession.model_validate((updated_record))

    def delete_one_by_id(self, id: UUID | str):
        if not self._exists_for_id(id=id):
            raise UserSessionFacade.NoResultFound

        delete_stmt = (
            delete(UserSessionDB)
            .where(UserSessionDB.id == id)
            .returning(UserSessionDB.id, UserSessionDB.user_id)
        )

        record = self.db_session.execute(delete_stmt).fetchone()

        return record

    def _one_exists(self, payload: Dict) -> bool:
        try:
            return self._exists_for_id(payload["id"])
        except (UserSessionFacade.NoResultFound, KeyError):
            pass

        try:
            return self._exists_for_user_id_and_auth_provider(
                user_id=payload["user_id"], auth_provider=payload["auth_provider"]
            )
        except KeyError:
            pass

        return False

    def _exists_for_id(self, id: UUID | str):
        try:
            user_session = (
                self.db_session.execute(
                    select(UserSessionDB.id).where(
                        UserSessionDB.id == id,
                    )
                )
                .scalars()
                .first()
            )
        except:
            pass

        return bool(user_session)

    def _exists_for_user_id_and_auth_provider(
        self, user_id: UUID | str, auth_provider: AuthProviderEnum
    ):
        try:
            user_session = (
                self.db_session.execute(
                    select(UserSessionDB.id).where(
                        and_(
                            UserSessionDB.auth_provider == auth_provider,
                            UserSessionDB.user_id == user_id,
                        )
                    )
                )
                .scalars()
                .first()
            )
        except:
            pass

        return bool(user_session)
