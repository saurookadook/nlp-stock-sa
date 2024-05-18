import arrow
from sqlalchemy import desc, literal_column, or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, List, Union
from uuid import UUID

from models.article_data import ArticleDataDB, ArticleData


class ArticleDataFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, id: Union[UUID, str]) -> ArticleData:
        try:
            article_data = self.db_session.execute(
                select(ArticleDataDB).where(ArticleDataDB.id == id)
            ).scalar_one()
        except NoResultFound:
            raise ArticleDataFacade.NoResultFound

        return ArticleData.model_validate(article_data)

    def get_one_by_source_url(self, source_url: str) -> ArticleData:
        return None

    def get_all_by_stock_symbol(self, quote_stock_symbol: str) -> List[ArticleData]:
        results = (
            self.db_session.execute(
                select(ArticleDataDB)
                .where(ArticleDataDB.quote_stock_symbol == quote_stock_symbol)
                .order_by(desc(ArticleDataDB.updated_at))
            )
            .scalars()
            .all()
        )

        return [ArticleData.model_validate(result) for result in results]

    def create_or_update(self, *, payload: Dict) -> ArticleData:
        maybe_one = self._find_one_if_exists(
            id=payload.get("id"), source_url=payload.get("source_url")
        )
        if maybe_one:
            return self.update(payload=payload)

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

    def update(self, *, payload: Dict) -> ArticleData:
        update_stmt = (
            update(ArticleDataDB)
            .where(
                or_(
                    ArticleDataDB.id == payload.get("id"),
                    ArticleDataDB.source_url == payload.get("source_url"),
                )
            )
            .values(**payload)
        ).returning(literal_column("*"))

        updated_record = self.db_session.execute(update_stmt).fetchone()
        self.db_session.flush()

        return ArticleData.model_validate(updated_record)

    def _find_one_if_exists(self, *, id, source_url):
        try:
            return self.get_one_by_id(id)
        except ArticleDataFacade.NoResultFound:
            pass

        try:
            return self.get_one_by_source_url(source_url)
        except ArticleDataFacade.NoResultFound:
            pass

        return None
