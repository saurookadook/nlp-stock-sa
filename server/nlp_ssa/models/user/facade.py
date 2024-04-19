import arrow
from sqlalchemy import literal_column, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from models.user import UserDB
from models.user.user import User


class UserFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, id):
        try:
            user = self.db_session.execute(
                select(UserDB).where(UserDB.id == id)
            ).scalar_one()
        except NoResultFound:
            raise UserFacade.NoResultFound

        return User.model_validate(user)

    def get_one_by_username(self, username):
        try:
            user = self.db_session.execute(
                select(UserDB).where(UserDB.username == username)
            ).scalar_one()
        except NoResultFound:
            raise UserFacade.NoResultFound

        return User.model_validate(user)

    def get_analysis_views_by_quote_stock_symbol(self, quote_stock_symbol: str):
        user_analysis_views = []
        # try:
        #     user_analysis_views = self.db_session.execute(
        #         select(UserDB)
        #     )
        # except Exception:
        #     raise

        return user_analysis_views

    def create_or_update(self, *, payload: Dict) -> User:
        # TODO: not sure this will still work?
        insert_stmt = insert(UserDB).values(**payload)

        full_stmt = insert_stmt.on_conflict_do_update(
            constraint=UserDB.__table__.primary_key,
            set_={
                **payload,
                "created_at": arrow.utcnow(),
                "updated_at": arrow.utcnow(),
            },
        ).returning(literal_column("*"))

        user = self.db_session.execute(full_stmt).fetchone()
        self.db_session.flush()

        return User.model_validate(user)
