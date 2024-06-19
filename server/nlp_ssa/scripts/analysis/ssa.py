import arrow
import logging
from sqlalchemy import and_, select
from typing import List
from vaderSentiment import vaderSentiment as vs
from uuid import UUID

from config.logging import ExtendedLogger, configure_logging
from constants import SentimentEnum
from db import db_session

from models.article_data import ArticleData, ArticleDataFacade
from models.sentiment_analysis import (
    SentimentAnalysisDB,
    SentimentAnalysisFacade,
)
from models.stock import StockDB
from models.user import UserFacade


configure_logging(app_name="stock_sentiment_analysis")
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


def get_fields_from_polarity_scores(
    polarity_scores_dict,
) -> tuple[float, SentimentEnum]:
    """TODO

    [Deriving single sentiment value from compound score](https://github.com/cjhutto/vaderSentiment?tab=readme-ov-file#about-the-scoring)
    - positive sentiment: compound score >= 0.05
    - neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
    - negative sentiment: compound score <= -0.05

    Args:
        `polarity_scores_dict`: Dictionary of polarity scores returned from the \
            `SentimentIntensityAnalyzer.polarity_scores` instance method
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

    return float(score), sentiment


def get_scores_and_create_rows(
    *,
    sia: vs.SentimentIntensityAnalyzer,
    article_data: List[ArticleData],
    quote_stock_symbol: str,
):
    """TODO: this needs a better name lol

    Args:
        `sia`: Instance of `SentimentIntensityAnalyzer` to be used to calculate polarity scores
        `article_data`: List of `article_data` records to be analyzed
        `quote_stock_symbol`: The quote stock symbol as a string. This is primarily just included or convenience.
    """
    sa_facade = SentimentAnalysisFacade(db_session=db_session)

    errored_total = 0
    for article_data_row in article_data:
        existing_sa_query = (
            db_session.execute(
                select(SentimentAnalysisDB).where(
                    and_(
                        SentimentAnalysisDB.source_group_id == article_data_row.id,
                        SentimentAnalysisDB.quote_stock_symbol
                        == article_data_row.quote_stock_symbol,
                    )
                )
            )
            .scalars()
            .all()
        )

        if len(existing_sa_query) > 1:
            logger.log_error_centered(
                " ERROR: results for existing sentiment_analyses records is greater than 1?? "
            )
            logger.error(
                f"source_group_id: {article_data_row.id}  |  quote_stock_symbol: {article_data_row.quote_stock_symbol}"
            )
            continue
        elif len(existing_sa_query) == 1:
            existing_sa = existing_sa_query[0]
            if isinstance(existing_sa.source_id, UUID):
                logger.log_warn_centered(
                    f" Skipping: sentiment_analysis record '{existing_sa.id}' is already up to date :] "
                )
                continue

            existing_sa_dict = dict(
                id=existing_sa.id,
                quote_stock_symbol=existing_sa.quote_stock_symbol,
                source_group_id=existing_sa.source_group_id,  # TODO: this is temporary until I get other tables and relationships created
                source_id=(
                    existing_sa.source_id
                    if isinstance(existing_sa.source_id, UUID)
                    else article_data_row.polymorphic_source.id
                ),
                output=existing_sa.output,
                score=existing_sa.score,
                sentiment=existing_sa.sentiment,
                created_at=existing_sa.created_at,
                updated_at=arrow.utcnow(),
            )

            sa_facade.create_or_update(payload=existing_sa_dict)
        else:
            polarity_scores_dict = sia.polarity_scores(article_data_row.sentence_tokens)
            score, sentiment = get_fields_from_polarity_scores(polarity_scores_dict)

            try:
                sentiment_analysis_record = dict(
                    quote_stock_symbol=article_data_row.quote_stock_symbol,
                    source_group_id=article_data_row.id,  # TODO: this is temporary until I get other tables and relationships created
                    source_id=article_data_row.polymorphic_source.id,
                    output=polarity_scores_dict,
                    score=score,
                    sentiment=sentiment,
                    created_at=arrow.utcnow(),
                    updated_at=arrow.utcnow(),
                )
                sa_facade.create_or_update(payload=sentiment_analysis_record)
            except Exception as e:
                logger.error(
                    f"ERROR in 'get_scores_and_create_rows' for '{quote_stock_symbol}'"
                    f" and article_data '{article_data_row.id}'"
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
            article_data=article_data,
            quote_stock_symbol=stock_symbol,
        )


if __name__ == "__main__":
    generate_sentiment_analyses_for_stocks()
