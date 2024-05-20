import arrow
import logging
import os
import re
from pprint import pprint as pretty_print
from sqlalchemy import select, update

from config import configure_logging
from db import db_session
from models.article_data import ArticleDataDB


configure_logging(app_name="clean_article_data")
logger = logging.getLogger(__file__)
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


def clean_article_data():
    article_data = []

    print_section_start("article_data")
    article_data_records = select(ArticleDataDB).execution_options(yield_per=20)

    for i, data_row in enumerate(db_session.scalars(article_data_records), start=1):
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

        db_session.execute(
            update(ArticleDataDB)
            .where(ArticleDataDB.id == data_row.id)
            .values(
                raw_content=cleaned_raw_content, sentence_tokens=cleaned_sentence_tokens
            )
        )

        if i % 20 == 0:
            logger.info(f"Committing at count '{i}'")
            # db_session.commit()
    db_session.commit()

    print_section_end("article_data", len(article_data))


if __name__ == "__main__":
    clean_article_data()
