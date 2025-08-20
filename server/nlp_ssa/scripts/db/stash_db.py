import arrow
import gzip
import json
import logging
from rich import inspect, pretty
from sqlalchemy import select
from uuid import UUID

from config import configure_logging
from constants import SentimentEnum, SourceDiscriminatorEnum
from db import db_session
from models.article_data import ArticleData, ArticleDataDB
from models.analysis_view import AnalysisView, AnalysisViewDB
from models.sentiment_analysis import SentimentAnalysis, SentimentAnalysisDB
from models.source import Source, SourceDB
from models.stock import Stock, StockDB
from models.user import User, UserDB


configure_logging(app_name="stash_db")
logger = logging.getLogger(__file__)


def stash_db():
    data = {
        "article_data": [],
        "analysis_views": [],
        "sentiment_analyses": [],
        "sources": [],
        "stocks": [],
        "users": [],
    }

    logger.log_info_section_start("article_data")
    article_data_records = db_session.execute(select(ArticleDataDB)).scalars().all()
    data["article_data"] = [
        ArticleData.model_validate(ad).model_dump(exclude={"polymorphic_source"})
        for ad in article_data_records
    ]
    logger.log_info_section_end("article_data", len(data["article_data"]))

    logger.log_info_section_start("analysis_views")
    analysis_view_records = db_session.execute(select(AnalysisViewDB)).scalars().all()
    data["analysis_views"] = [
        AnalysisView.model_validate(av).model_dump() for av in analysis_view_records
    ]
    logger.log_info_section_end("analysis_views", len(data["analysis_views"]))

    logger.log_info_section_start("sentiment_analyses")
    sentiment_analysis_records = (
        db_session.execute(select(SentimentAnalysisDB)).scalars().all()
    )
    data["sentiment_analyses"] = [
        SentimentAnalysis.model_validate(sa).model_dump(exclude={"source"})
        for sa in sentiment_analysis_records
    ]
    logger.log_info_section_end("sentiment_analyses", len(data["sentiment_analyses"]))

    logger.log_info_section_start("sources")
    sources_records = db_session.execute(select(SourceDB)).scalars().all()
    data["sources"] = [
        Source.model_validate(src).model_dump(exclude={"data"})
        for src in sources_records
    ]
    logger.log_info_section_end("sources", len(data["sources"]))

    logger.log_info_section_start("stocks")
    stock_records = db_session.execute(select(StockDB)).scalars().all()
    data["stocks"] = [Stock.model_validate(stk).model_dump() for stk in stock_records]
    logger.log_info_section_end("stocks", len(data["stocks"]))

    logger.log_info_section_start("user")
    user_records = db_session.execute(select(UserDB)).scalars().all()
    data["users"] = [User.model_validate(usr).model_dump() for usr in user_records]
    logger.log_info_section_end("user", len(data["users"]))

    db_session.close()

    enum_types_tuple = tuple([SentimentEnum, SourceDiscriminatorEnum])

    logger.log_info_centered(" 'Making the data serializable...'  ")
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
