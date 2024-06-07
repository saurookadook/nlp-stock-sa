import arrow
import logging
from sqlalchemy import select
from typing import List
from vaderSentiment import vaderSentiment as vs
from uuid import UUID, uuid4

from config.logging import ExtendedLogger, configure_logging
from db import db_session

# from models.analysis_view import AnalysisViewFacade
from models.article_data import ArticleData, ArticleDataFacade
from models.sentiment_analysis import SentimentAnalysis, SentimentAnalysisFacade
from models.sentiment_analysis.constants import SentimentEnum
from models.stock import StockDB
from models.user import UserFacade


configure_logging(app_name="stash_db")
logger: ExtendedLogger = logging.getLogger(__file__)


user_facade = UserFacade(db_session=db_session)

andrea = user_facade.get_one_by_username(username="ovalle15")
andy = user_facade.get_one_by_username(username="saurookadook")


def log_created_rows_results_by_stock(
    *, quote_stock_symbol: str, errored_total: int, total: int
):
    log_lines = [
        f"'sentiment_analyses' created for '{quote_stock_symbol}'",
        f"---- Successful: {total - errored_total}",
        f"---- Errored: {errored_total}",
        f"---- Total: {total}",
    ]

    for line in log_lines:
        logger.info(line.ljust(60).center(120, "="))


def get_fields_from_polarity_scores(polarity_scores_dict):
    """TODO

    [Deriving single sentiment value from compound score](https://github.com/cjhutto/vaderSentiment?tab=readme-ov-file#about-the-scoring)
    - positive sentiment: compound score >= 0.05
    - neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
    - negative sentiment: compound score <= -0.05

    Args:
        `polarity_scores_dict`: _description_
    """
    score = 0
    sentiment = SentimentEnum.COMPOUND

    compound_score = polarity_scores_dict.get("compound")

    if compound_score >= 0.05:
        score = polarity_scores_dict.get("pos")
        sentiment = SentimentEnum.POSITIVE
    elif compound_score > -0.05 and compound_score < 0.05:
        score = polarity_scores_dict.get("neu")
        sentiment = SentimentEnum.NEUTRAL
    elif compound_score <= -0.05:
        score = polarity_scores_dict.get("neg")
        sentiment = SentimentEnum.NEGATIVE
    else:
        logger.warn(
            f"get_fields_from_polarity_scores: Somethin's borked up with this compound_score '{compound_score}'"
        )

    return score, sentiment


def get_scores_and_create_rows(
    *,
    sia: vs.SentimentIntensityAnalyzer,
    quote_stock_symbol: str,
    source_group_id: UUID,
    article_data: List[ArticleData],
):
    """TODO: this needs a better name lol

    Args:
        `sia`: _description_
        `quote_stock_symbol`: _description_
        `source_group_id`: _description_
        `article_data`: _description_
    """
    sa_facade = SentimentAnalysisFacade(db_session=db_session)

    errored_total = 0
    for data in article_data:
        polarity_scores_dict = sia.polarity_scores(data.sentence_tokens)
        score, sentiment = get_fields_from_polarity_scores(polarity_scores_dict)

        try:
            sentiment_analysis_record = SentimentAnalysis(
                id=uuid4(),
                quote_stock_symbol=quote_stock_symbol,
                source_group_id=data.id,  # TODO: this is temporary until I get other tables and relationships created
                output=polarity_scores_dict,
                score=score,
                sentiment=sentiment,
                created_at=arrow.utcnow(),
                updated_at=arrow.utcnow(),
            )
            sa_facade.create_or_update(payload=sentiment_analysis_record.model_dump())
        except Exception as e:
            logger.error(
                f"ERROR in 'get_scores_and_create_rows' for '{quote_stock_symbol}' and article_data '{data.id}'"
            )
            logger.error(e)
            errored_total += 1

        db_session.commit()

    log_created_rows_results_by_stock(
        quote_stock_symbol=quote_stock_symbol,
        errored_total=errored_total,
        total=len(article_data),
    )


def generate_sentiment_analyses_for_stocks():
    stock_symbol_slugs_query = db_session.execute(
        select(StockDB.quote_stock_symbol)
    ).all()

    if not stock_symbol_slugs_query:
        raise Exception("generate_sentiment_analyses_for_stocks: No stocks found :[")

    sia = vs.SentimentIntensityAnalyzer()
    article_data_facade = ArticleDataFacade(db_session=db_session)

    for row in stock_symbol_slugs_query:
        stock_symbol = row[0]
        logger.info(f"Generating analyses for stock '{stock_symbol}'...")
        article_data = article_data_facade.get_all_by_stock_symbol(
            quote_stock_symbol=stock_symbol
        )

        if not article_data:
            continue

        get_scores_and_create_rows(
            sia=sia,
            quote_stock_symbol=stock_symbol,
            source_group_id=uuid4(),
            article_data=article_data,
        )


if __name__ == "__main__":
    generate_sentiment_analyses_for_stocks()
