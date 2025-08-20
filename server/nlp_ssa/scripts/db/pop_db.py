import gzip
import json
import logging
from rich import inspect, pretty

from config import configure_logging
from db import db_session
from models import *
from models.analysis_view import AnalysisView, AnalysisViewFacade
from models.article_data import ArticleData, ArticleDataFacade
from models.sentiment_analysis import SentimentAnalysis, SentimentAnalysisFacade
from models.stock import Stock, StockFacade


configure_logging(app_name="pop_db")
logger = logging.getLogger(__file__)


def populate_db():
    f = gzip.open("nlp_ssa/scripts/db/states/db_state.json.gz", "rb")
    data = json.loads(f.read().decode("utf-8"))
    f.close()

    EXCLUDABLE_FIELDS_SET = {"polymorphic_source", "source"}
    # inspect(inspect)
    # inspect(data, all=True)

    logger.log_info_section_start("stocks")
    stock_facade = StockFacade(db_session=db_session)
    for i, data_row in enumerate(data["stocks"]):
        print(f"stock - {i}: {data_row['quote_stock_symbol']}")
        # inspect(data_row, help=True)
        stock_model = Stock.model_validate(data_row)
        # inspect(stock_model, help=True)
        stock_payload = dict(**stock_model.model_dump())
        # inspect(stock_payload, help=True)
        stock_facade.create_or_update(payload=stock_payload)
        db_session.commit()
    logger.log_info_section_end("stocks", len(data["stocks"]))

    logger.log_info_section_start("article_data")
    article_data_facade = ArticleDataFacade(db_session=db_session)
    for i, data_row in enumerate(data["article_data"]):
        print(f"article_data - {i}: {data_row['source_url']}")
        # inspect(data_row, help=True)
        article_data_model = ArticleData.model_validate(data_row)
        # inspect(article_data_model, help=True)
        article_data_payload = dict(
            **article_data_model.model_dump(exclude=EXCLUDABLE_FIELDS_SET)
        )
        # pretty.pprint(article_data_payload, expand_all=True)
        article_data_facade.create_or_update(payload=article_data_payload)
        db_session.commit()
    logger.log_info_section_end("article_data", len(data["article_data"]))

    logger.log_info_section_start("sentiment_analyses")
    sentiment_analysis_facade = SentimentAnalysisFacade(db_session=db_session)
    for i, data_row in enumerate(data["sentiment_analyses"]):
        print(f"sentiment_analysis - {i}: {data_row['source_group_id']}")
        # inspect(data_row, help=True)
        sentiment_analysis_model = SentimentAnalysis.model_validate(data_row)
        # inspect(sentiment_analysis_model, help=True)
        sentiment_analysis_payload = dict(
            **sentiment_analysis_model.model_dump(exclude=EXCLUDABLE_FIELDS_SET)
        )
        # pretty.pprint(article_data_payload, expand_all=True)
        sentiment_analysis_facade.create_or_update(payload=sentiment_analysis_payload)
        db_session.commit()
    logger.log_info_section_end("sentiment_analyses", len(data["sentiment_analyses"]))

    # TODO: add this once `analysis_views` are fully implemented :]
    # logger.log_info_section_start("analysis_views")
    # analysis_view_facade = AnalysisViewFacade(db_session=db_session)
    # for i, data_row in enumerate(data["analysis_views"]):
    #     print(f"analysis_view - {i}: {data_row['source_group_id']}")
    #     # inspect(data_row, help=True)
    #     analysis_view_model = AnalysisView.model_validate(data_row)
    #     # inspect(analysis_view_model, help=True)
    #     analysis_view_facade.create_or_update(
    #         payload=dict(**analysis_view_model.model_dump())
    #     )
    #     db_session.commit()
    # logger.log_info_section_end("analysis_views", len(data["analysis_views"]))

    db_session.close()


if __name__ == "__main__":
    populate_db()
