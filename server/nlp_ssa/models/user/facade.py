from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from models.user import UserDB


class UserFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, id):

        try:
            sentiment_analysis = self.db_session.execute(
                select(UserDB).where(id=id)
            ).scalar_one()
        except NoResultFound:
            raise UserFacade.NoResultFound

        # return User.from_orm(sentiment_analysis)
        return sentiment_analysis
