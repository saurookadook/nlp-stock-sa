# flake8: noqa
import logging
from pprint import pprint as pretty_print
from rich import inspect
from sqlalchemy import select, delete

from config import configure_logging
from config.logging import ExtendedLogger
from db import db_session
from models.article_data import ArticleDataDB, ArticleDataFacade
from models.sentiment_analysis import SentimentAnalysisDB, SentimentAnalysisFacade


configure_logging(app_name="delete_orphaned_sentiment_analyses")
logger: ExtendedLogger = logging.getLogger(__file__)


def run_delete_orphaned_sentiment_analyses():
    article_data_facade = ArticleDataFacade(db_session=db_session)
    sentiment_analysis_facade = SentimentAnalysisFacade(db_session=db_session)

    sa_stmt = select(SentimentAnalysisDB).execution_options(yield_per=10)

    orphaned_sa_ids = []

    for i, sa in enumerate(db_session.scalars(sa_stmt)):
        if sa.source is not None and sa.source.data is not None:
            logger.info(
                f"sa '{str(sa.id)}' has source '{str(sa.source.data_type_id)}' of type '{str(sa.source.data_type.value)}'"
            )
        else:
            logger.log_info_centered(f" sa: {i} ")
            inspect(sa, methods=True, sort=True)
            orphaned_sa_ids.append(sa.id)
            # breakpoint()

    logger.log_info_centered(" orphaned_sa_ids ")
    pretty_print(orphaned_sa_ids, indent=4)

    del_stmt = (
        delete(SentimentAnalysisDB)
        .where(SentimentAnalysisDB.id.in_(orphaned_sa_ids))
        .returning(SentimentAnalysisDB.id)
    )
    deleted = db_session.execute(del_stmt).scalars().all()

    logger.info(f"        DELETED {len(deleted)} SENTIMENT_ANALYSES RECORDS")
    inspect(deleted, methods=True, sort=True)
    db_session.commit()


if __name__ == "__main__":
    run_delete_orphaned_sentiment_analyses()
