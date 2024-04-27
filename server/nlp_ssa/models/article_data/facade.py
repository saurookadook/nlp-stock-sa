import arrow
from sqlalchemy import literal_column, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, Union
from uuid import UUID

from models.article_data import ArticleDataDB, ArticleData


class ArticleDataFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, id: Union[UUID, str]):
        try:
            article_data = self.db_session.execute(
                select(ArticleDataDB).where(ArticleDataDB.id == UUID(id))
            ).scalar_one()
        except NoResultFound:
            raise ArticleDataFacade.NoResultFound

        return ArticleData.model_validate(article_data)

    def create_or_update(self, *, payload: Dict) -> ArticleData:
        insert_stmt = insert(ArticleDataDB).values(**payload)

        full_stmt = insert_stmt.on_conflict_do_update(
            constraint=ArticleDataDB.__table__.primary_key,
            set_={
                **payload,
                # "created_at": arrow.utcnow(),
                "updated_at": arrow.utcnow(),
            },
        ).returning(literal_column("*"))

        article_data = self.db_session.execute(full_stmt).fetchone()
        self.db_session.flush()

        return ArticleData.model_validate(article_data)