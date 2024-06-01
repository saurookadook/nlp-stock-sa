import arrow
from uuid import UUID
from sqlalchemy import desc, literal_column, or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, List

from models.sentiment_analysis import SentimentAnalysisDB
from models.sentiment_analysis.sentiment_analysis import SentimentAnalysis


class SentimentAnalysisFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, row_id: str | UUID) -> SentimentAnalysis:
        try:
            sentiment_analysis = self.db_session.execute(
                select(SentimentAnalysisDB).where(SentimentAnalysisDB.id == row_id)
            ).scalar_one()
        except NoResultFound:
            raise SentimentAnalysisFacade.NoResultFound

        return SentimentAnalysis.model_validate(sentiment_analysis)

    def get_one_by_source_group_id(
        self, source_group_id: str | UUID
    ) -> SentimentAnalysis:
        try:
            sentiment_analysis = self.db_session.execute(
                select(SentimentAnalysisDB).where(
                    SentimentAnalysisDB.source_group_id == source_group_id
                )
            ).scalar_one()
        except NoResultFound:
            raise SentimentAnalysisFacade.NoResultFound

        return SentimentAnalysis.model_validate(sentiment_analysis)

    def get_all_by_stock_symbol(
        self, quote_stock_symbol: str
    ) -> List[SentimentAnalysis]:
        results = (
            self.db_session.execute(
                select(SentimentAnalysisDB)
                .where(SentimentAnalysisDB.quote_stock_symbol == quote_stock_symbol)
                .order_by(desc(SentimentAnalysisDB.updated_at))
            )
            .scalars()
            .all()
        )

        return [SentimentAnalysis.model_validate(result) for result in results]

    def create_or_update(self, *, payload: Dict) -> SentimentAnalysis:
        maybe_one = self._find_one_if_exists(
            row_id=payload.get("id"), source_group_id=payload.get("source_group_id")
        )
        if maybe_one:
            return self.update(payload=payload)

        insert_stmt = insert(SentimentAnalysisDB).values(**payload)

        full_stmt = insert_stmt.on_conflict_do_update(
            constraint=SentimentAnalysisDB.__table__.primary_key,
            set_=dict(**payload, updated_at=arrow.utcnow()),
        ).returning(literal_column("*"))

        sentiment_analysis = self.db_session.execute(full_stmt).fetchone()
        self.db_session.flush()

        return SentimentAnalysis.model_validate(sentiment_analysis)

    def update(self, *, payload: Dict) -> SentimentAnalysis:
        update_stmt = (
            update(SentimentAnalysisDB)
            .where(
                or_(
                    SentimentAnalysisDB.id == payload.get("id"),
                    SentimentAnalysisDB.source_group_id
                    == payload.get("source_group_id"),
                )
            )
            .values(**payload)
        ).returning(literal_column("*"))

        updated_record = self.db_session.execute(update_stmt).fetchone()
        self.db_session.flush()

        return SentimentAnalysis.model_validate(updated_record)

    def _find_one_if_exists(
        self, *, row_id: str | UUID = None, source_group_id: str | UUID = None
    ):
        try:
            return self.get_one_by_id(row_id)
        except SentimentAnalysisFacade.NoResultFound:
            pass

        try:
            return self.get_one_by_source_group_id(source_group_id)
        except SentimentAnalysisFacade.NoResultFound:
            pass

        return None
