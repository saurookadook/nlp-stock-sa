from uuid import UUID
from sqlalchemy import select
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
        return []

    def create_or_update(self, *, payload: Dict) -> SentimentAnalysis:
        pass

    def update(self, *, payload: Dict) -> SentimentAnalysis:
        pass

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
