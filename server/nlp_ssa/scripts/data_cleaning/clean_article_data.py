import logging
import re
from sqlalchemy import select

from config import configure_logging
from config.logging import ExtendedLogger
from db import db_session
from models.article_data import ArticleDataDB, ArticleDataFacade
from models.stock import StockDB
from models.sentiment_analysis import SentimentAnalysisDB


configure_logging(app_name="clean_article_data")
logger: ExtendedLogger = logging.getLogger(__file__)


def clean_article_data():
    article_data_facade = ArticleDataFacade(db_session=db_session)
    cleaned_total = 0

    logger.log_info_section_start("article_data")
    article_data_records = select(ArticleDataDB).execution_options(
        populate_existing=True, yield_per=20
    )

    for i, data_row in enumerate(db_session.scalars(article_data_records), start=1):
        try:
            logger.info(f"Index: {i}, Source URL: {data_row.source_url}")
            cleaned_raw_content = re.sub(
                r"(^{\")|(view\scomments(\"})?$)",
                "",
                data_row.raw_content,
                flags=re.IGNORECASE | re.MULTILINE,
            )
            cleaned_sentence_tokens = re.sub(
                r"(^{\")|(view\scomments(\"})?$)",
                "",
                data_row.sentence_tokens,
                flags=re.IGNORECASE | re.MULTILINE,
            )

            article_data_facade.create_or_update(
                payload=dict(
                    id=data_row.id,
                    raw_content=cleaned_raw_content,
                    sentence_tokens=cleaned_sentence_tokens,
                )
            )

            if i % 20 == 0:
                logger.info(f"At count '{i}'")
                # db_session.commit()
            cleaned_total = i
        except Exception as e:
            logger.log_error_centered(
                f" ERROR at index {i} for article_data: {data_row.id} "
            )
            logger.log_error_centered(e)
            db_session.commit()
    db_session.commit()

    logger.log_info_section_end("article_data", cleaned_total)


if __name__ == "__main__":
    clean_article_data()
