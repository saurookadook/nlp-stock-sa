# flake8: noqa
import logging
from bdb import BdbQuit
from pprint import pprint as pretty_print
from rich import inspect
from sqlalchemy import select
from uuid import UUID

from config import configure_logging
from config.logging import ExtendedLogger
from constants import SentimentEnum
from db import db_session
from models.article_data import ArticleDataDB, ArticleDataFacade
from models.analysis_view import AnalysisViewDB, AnalysisViewFacade
from models.sentiment_analysis import SentimentAnalysisDB, SentimentAnalysisFacade
from models.source import SourceDB, Source
from models.stock import StockDB, StockFacade
from models.user import UserDB, UserFacade


configure_logging(app_name="stash_db")
logger: ExtendedLogger = logging.getLogger(__file__)


def start_sandbox():
    article_data_facade = ArticleDataFacade(db_session=db_session)
    analysis_view_facade = AnalysisViewFacade(db_session=db_session)
    sentiment_analysis_facade = SentimentAnalysisFacade(db_session=db_session)
    stock_facade = StockFacade(db_session=db_session)
    user_facade = UserFacade(db_session=db_session)

    logger.log_info_centered(" Starting sandbox!! ")

    try:
        breakpoint()
    except BdbQuit:
        pass

    logger.log_info_centered(" Stopping sandbox... ")


if __name__ == "__main__":
    start_sandbox()
