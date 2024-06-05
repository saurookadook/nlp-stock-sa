import logging
from fastapi import APIRouter, Depends, Request
from rich import inspect

from api.routes.api.article_data.models import (
    ArticleDataResponse,
    ArticleDataBySlugResponse,
)
from api.routes.api.article_data.route_handlers import (
    get_all_article_data,
    get_article_data_by_stock_slug,
)
from api.routes.auth.session.caching import safe_get_from_session_cache
from config.logging import ExtendedLogger
from db import db_session


logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


@router.get("/api/article-data/{stock_slug}", response_model=ArticleDataBySlugResponse)
async def read_article_data_by_slug(stock_slug: str):
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


def maybe_get_user_from_cache(request: Request):
    maybe_user_from_cache = safe_get_from_session_cache(
        cache_key="session|saurookadook"
    )

    print(" maybe_user_from_cache ".center(120, "="))
    inspect(maybe_user_from_cache, sort=True)

    return maybe_user_from_cache


@router.get("/api/article-data", response_model=ArticleDataResponse)
async def read_article_data(maybe_user_from_cache=Depends(maybe_get_user_from_cache)):
    """Endpoint for getting all article data.

    Query results are
    - limited to 30
    - grouped by stock slug
    - ordered by date_modified (published date?) descending
    """

    article_data_grouped_by_stock_slug = []

    try:
        article_data_grouped_by_stock_slug = get_all_article_data(db_session=db_session)
    except Exception as e:
        logger.error(e)
        # raise

    return {"data": article_data_grouped_by_stock_slug}
