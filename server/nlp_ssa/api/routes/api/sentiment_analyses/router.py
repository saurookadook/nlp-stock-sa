import logging
from fastapi import APIRouter, Depends, Request

from api.routes.api.sentiment_analyses.models import SentimentAnalysesBySlugResponse
from api.routes.api.sentiment_analyses.route_handlers import (
    get_all_sentiment_analyses_by_stock_slug,
)
from config import env_vars
from config.logging import ExtendedLogger
from db import db_session


logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


@router.get(
    "/api/sentiment-analyses/{stock_slug}",
    response_model=SentimentAnalysesBySlugResponse,
)
async def read_sentiment_analyses_by_slug(stock_slug: str):
    sentiment_analyses_rows = []

    try:
        sentiment_analyses_rows = get_all_sentiment_analyses_by_stock_slug(
            db_session=db_session, stock_slug=stock_slug
        )
    except Exception as e:
        logger.error(e)

    return {
        "data": {
            "quote_stock_symbol": stock_slug,
            "sentiment_analyses": sentiment_analyses_rows,
        }
    }
