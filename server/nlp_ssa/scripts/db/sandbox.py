# flake8: noqa
import logging
from pprint import pprint as pretty_print
from rich import inspect
from sqlalchemy import select
from uuid import UUID

from config import configure_logging
from constants import SentimentEnum
from db import db_session
from models.article_data import ArticleDataDB
from models.analysis_view import AnalysisViewDB
from models.sentiment_analysis import SentimentAnalysisDB
from models.stock import StockDB
from models.user import UserDB


configure_logging(app_name="stash_db")
logger = logging.getLogger(__file__)


def start_sandbox():
    pass


if __name__ == "__main__":
    start_sandbox()
