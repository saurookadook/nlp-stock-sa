import logging
from fastapi import APIRouter, Depends, Request
from rich import inspect, pretty

from api.dependencies.user_session import handle_user_session
from api.routes.api.article_data.models import (
    ArticleDataResponse,
    ArticleDataBySlugResponse,
)
from api.routes.api.article_data.route_handlers import (
    get_all_article_data,
    get_article_data_by_stock_slug,
)
from api.routes.auth.session.caching import build_cache_key, safe_get_from_session_cache
from config import env_vars
from config.logging import ExtendedLogger
from db import db_session


logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


@router.get("/api/article-data/{stock_slug}", response_model=ArticleDataBySlugResponse)
async def read_article_data_by_slug(
    stock_slug: str, user_session=Depends(handle_user_session)
):
    logger.log_debug_centered(
        " read_article_data_by_slug - user_session ", fill_char="+"
    )
    logger.log_debug_pretty(user_session)
    logger.log_debug_centered("", fill_char="+")

    article_data_rows = []

    try:
        article_data_rows = get_article_data_by_stock_slug(
            db_session=db_session, stock_slug=stock_slug
        )
    except Exception as e:
        logger.error(e)

    return {
        "data": {"quote_stock_symbol": stock_slug, "article_data": article_data_rows}
    }


@router.get("/api/article-data", response_model=ArticleDataResponse)
async def read_article_data(user_session=Depends(handle_user_session)):
    """Endpoint for getting all article data.

    Query results are
    - limited to 30
    - grouped by stock slug
    - ordered by date_modified (published date?) descending
    """

    logger.log_debug_centered(" read_article_data - user_session ", fill_char="+")
    logger.log_debug_pretty(user_session)
    logger.log_debug_centered("", fill_char="+")

    article_data_grouped_by_stock_slug = []

    try:
        article_data_grouped_by_stock_slug = get_all_article_data(db_session=db_session)
    except Exception as e:
        logger.error(e)
        # raise

    return {"data": article_data_grouped_by_stock_slug}
