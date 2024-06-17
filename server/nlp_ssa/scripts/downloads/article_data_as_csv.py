import csv
import logging
from sqlalchemy import select

from config import configure_logging
from db import db_session
from models.article_data import ArticleDataDB


configure_logging(app_name="article_data_as_csv")
logger = logging.getLogger(__file__)


def download_article_data_as_csv():
    with open(
        "nlp_ssa/scripts/downloads/files/article_data.csv", "w", newline=""
    ) as csvfile:
        fieldnames = [c.key for c in ArticleDataDB.__table__.columns]

        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        logger.log_info_section_start("article_data")
        total_count = 0
        article_data_records_stmt = select(ArticleDataDB).execution_options(
            yield_per=20
        )
        article_data = []
        for i, data_row in enumerate(
            db_session.scalars(article_data_records_stmt), start=1
        ):
            ad = data_row.__dict__

            try:
                del ad["_sa_instance_state"]
            except KeyError:
                pass

            article_data.append(ad)

            logger.log_info_centered(f" Writing '{i}' rows... ")
            csv_writer.writerow(ad)
            total_count = i

        logger.log_info_section_end("article_data", total_count)


if __name__ == "__main__":
    download_article_data_as_csv()
