import arrow
from sqlalchemy import and_, literal_column, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from uuid import UUID

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

    def get_analysis_views_by_quote_stock_symbol(
        self, user_id: UUID, quote_stock_symbol: str
    ):
        from models.analysis_view.db import AnalysisViewDB
        from models.sentiment_analysis.db import SentimentAnalysisDB

        user_analysis_views = []

        user_analysis_views = (
            self.db_session.execute(
                select(AnalysisViewDB)
                .join(
                    SentimentAnalysisDB,
                    SentimentAnalysisDB.source_group_id
                    == AnalysisViewDB.source_group_id,
                )
                .where(
                    and_(
                        SentimentAnalysisDB.quote_stock_symbol == quote_stock_symbol,
                        AnalysisViewDB.user_id == user_id,
                    )
                )
            )
            .scalars()
            .all()
        )

        return user_analysis_views

    def create_or_update(self, *, payload: Dict) -> User:
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
