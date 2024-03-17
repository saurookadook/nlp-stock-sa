from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

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
