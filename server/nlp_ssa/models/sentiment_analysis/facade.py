import arrow
from rich import inspect, pretty
from sqlalchemy import asc, or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, List
from uuid import UUID

from constants import SourceDiscriminatorEnum
from models.sentiment_analysis.db import SentimentAnalysisDB
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
        # TODO: update this method to get by source_id?
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
        """Returns list of `SentimentAnalysis` instances by `updated_at` in ascending ordered

        Args:
            `quote_stock_symbol`: Quote stock symbol as a string.

        Returns:
            `List[SentimentAnalysis]`:
        """

        results = (
            self.db_session.execute(
                select(SentimentAnalysisDB)
                .where(SentimentAnalysisDB.quote_stock_symbol == quote_stock_symbol)
                .order_by(asc(SentimentAnalysisDB.updated_at))
            )
            .scalars()
            .all()
        )

        return [SentimentAnalysis.model_validate(result) for result in results]

    def create_or_update(self, *, payload: Dict) -> SentimentAnalysis:
        prepared_payload = self._prepare_payload(payload)

        maybe_one = self._find_one_if_exists(
            row_id=prepared_payload.get("id"),
            source_id=prepared_payload.get("source_id"),
        )
        if maybe_one:
            return self.update(payload=prepared_payload)

        prepared_payload.setdefault("updated_at", arrow.utcnow())

        insert_stmt = insert(SentimentAnalysisDB).values(**prepared_payload)

        full_stmt = insert_stmt.on_conflict_do_update(
            constraint=SentimentAnalysisDB.__table__.primary_key,
            set_=dict(**prepared_payload),
        ).returning(SentimentAnalysisDB)

        sentiment_analysis = self.db_session.execute(full_stmt).scalar_one()
        self.db_session.flush()

        return SentimentAnalysis.model_validate(sentiment_analysis)

    def update(self, *, payload: Dict) -> SentimentAnalysis:
        update_stmt = (
            update(SentimentAnalysisDB)
            .where(
                or_(
                    SentimentAnalysisDB.id == payload.get("id"),
                    SentimentAnalysisDB.source_id == payload.get("source_id"),
                )
            )
            .values(**payload)
        ).returning(SentimentAnalysisDB)

        updated_record = self.db_session.execute(update_stmt).scalar_one()
        self.db_session.flush()

        return SentimentAnalysis.model_validate(updated_record)

    # TODO: this can be WAY more efficient (it doesn't need to return a whole row)
    def _find_one_if_exists(
        self, *, row_id: str | UUID = None, source_id: str | UUID = None
    ):
        try:
            return self.get_one_by_id(row_id)
        except SentimentAnalysisFacade.NoResultFound:
            pass

        # TODO: add this method...?
        # try:
        #     return self.get_one_by_source_id(source_id)
        # except SentimentAnalysisFacade.NoResultFound:
        #     pass

        return None

    def _prepare_payload(self, payload):
        source = payload.get("source", None)
        # TODO: this conditional should probably be put into a method :]
        if source is None:
            payload.pop("source", None)
        elif source.data_type in SourceDiscriminatorEnum:
            payload.setdefault("source_id", source.id)
            payload.pop("source", None)

        return payload
