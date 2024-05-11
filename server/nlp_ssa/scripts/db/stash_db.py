import arrow
import gzip
import json
import logging
import os
from sqlalchemy import select
from uuid import UUID

from config import configure_logging
from db import db_session
from models.article_data import ArticleDataDB
from models.analysis_view import AnalysisViewDB
from models.sentiment_analysis import SentimentAnalysisDB, SentimentEnum
from models.stock import StockDB
from models.user import UserDB


logger = logging.getLogger(__name__)
raw_window_width, _ = os.get_terminal_size()
window_width = (
    raw_window_width - 80
)  # to account for characters added by logging handlers


def print_section_start(entity_name: str):
    logger.info(f" 'Getting `{entity_name}` records...' ".center(window_width, "="))


def print_section_end(entity_name: str, entity_count: int):
    logger.info(
        f" 'Done retrieving `{entity_name}` records! Total: {entity_count}' ".center(
            window_width, "="
        )
    )


def stash_db():
    data = {
        "article_data": [],
        "analysis_views": [],
        "sentiment_analyses": [],
        "stocks": [],
        "users": [],
    }

    print_section_start("article_data")
    article_data_records = db_session.execute(select(ArticleDataDB)).scalars().all()
    # TODO: is there something else from SQLAlchemy that would be better than __dict__
    data["article_data"] = [ad.__dict__ for ad in article_data_records]
    print_section_end("article_data", len(data["article_data"]))

    print_section_start("analysis_view")
    analysis_view_records = db_session.execute(select(AnalysisViewDB)).scalars().all()
    data["analysis_view"] = [ad.__dict__ for ad in analysis_view_records]
    print_section_end("analysis_view", len(data["analysis_view"]))

    print_section_start("sentiment_analysis")
    sentiment_analysis_records = (
        db_session.execute(select(SentimentAnalysisDB)).scalars().all()
    )
    data["sentiment_analyses"] = [ad.__dict__ for ad in sentiment_analysis_records]
    print_section_end("sentiment_analysis", len(data["sentiment_analyses"]))

    print_section_start("stock")
    stock_records = db_session.execute(select(StockDB)).scalars().all()
    data["stocks"] = [ad.__dict__ for ad in stock_records]
    print_section_end("stock", len(data["stocks"]))

    print_section_start("user")
    user_records = db_session.execute(select(UserDB)).scalars().all()
    data["users"] = [ad.__dict__ for ad in user_records]
    print_section_end("user", len(data["users"]))

    db_session.close()

    enum_types_tuple = SentimentEnum

    logger.info(" 'Making the data serializable...'  ".center(window_width, "="))
    for key in data:
        for x in data.get(key):
            try:
                del x["_sa_instance_state"]
            except KeyError:
                pass

            for k, v in x.items():
                if isinstance(v, (arrow.Arrow, UUID)):
                    x[k] = str(v)
                elif isinstance(v, list):
                    new_list = []

                    for list_item in v:
                        if isinstance(list_item, (arrow.Arrow, UUID)):
                            new_list.append(str(list_item))
                    x[k] = x[k] if len(new_list) == 0 else new_list
                if isinstance(v, enum_types_tuple):
                    x[k] = v.value

    with gzip.open("nlp_ssa/scripts/db/states/db_state.json.gz", "wb") as outfile:
        try:
            stringified_json = json.dumps(data, indent=4)
            outfile.write(stringified_json.encode("utf-8"))
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    stash_db()
