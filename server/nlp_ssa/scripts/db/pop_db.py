import gzip
import json
import logging
from rich import inspect

from config import configure_logging
from db import db_session
from models.analysis_view import AnalysisViewFacade
from models.article_data import ArticleDataFacade
from models.sentiment_analysis import SentimentAnalysisFacade
from models.stock import StockFacade


configure_logging(app_name="pop_db")
logger = logging.getLogger(__file__)


def populate_db():
    f = gzip.open("nlp_ssa/scripts/db/states/db_state.json.gz", "rb")
    data = json.loads(f.read().decode("utf-8"))
    f.close()

    inspect(data, all=True)

    logger.log_info_section_start("stock")
    stock_facade = StockFacade(db_session=db_session)
    for i, data_row in enumerate(data["stock"]):
        print(f"stock - {i}: {data_row.quote_stock_symbol}")
        stock_facade.create_or_update(payload=data_row)
        db_session.commit()
    logger.log_info_section_end("stock", len(data["stock"]))

    logger.log_info_section_start("article_data")
    article_data_facade = ArticleDataFacade(db_session=db_session)
    for i, data_row in enumerate(data["article_data"]):
        print(f"article_data - {i}: {data_row.source_url}")
        article_data_facade.create_or_update(payload=data_row)
        db_session.commit()
    logger.log_info_section_end("article_data", len(data["article_data"]))

    # logger.log_info_section_start("sentiment_analysis")
    # sentiment_analysis_facade = SentimentAnalysisFacade(db_session=db_session)
    # for i, data_row in enumerate(data["sentiment_analyses"]):
    #     print(f"sentiment_analysis - {i}: {data_row.source_group_id}")
    #     sentiment_analysis_facade.create_or_update(payload=data_row)
    #     db_session.commit()
    # logger.log_info_section_end("sentiment_analysis", len(data["sentiment_analyses"]))

    # logger.log_info_section_start("analysis_view")
    # analysis_view_facade = AnalysisViewFacade(db_session=db_session)
    # for i, data_row in enumerate(data["analysis_view"]):
    #     print(f"analysis_view - {i}: {data_row.source_group_id}")
    #     analysis_view_facade.create_or_update(payload=data_row)
    #     db_session.commit()
    # logger.log_info_section_end("analysis_view", len(data["analysis_view"]))


if __name__ == "__main__":
    populate_db()
