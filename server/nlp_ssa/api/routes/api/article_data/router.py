import logging
from fastapi import APIRouter

from api.routes.api.article_data.models import ArticleDataResponse
from api.routes.api.article_data.route_handlers import (
    get_all_article_data,
    get_article_data_by_stock_slug,
)
from config import configure_logging
from db import db_session

# configure_logging(app_name="nlp_ssa.api.routes.article_data")
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/article-data/{stock_slug}", response_model=ArticleDataResponse)
async def read_article_data_by_slug(stock_slug: str):
    article_data_rows = []

    try:
        article_data_rows = get_article_data_by_stock_slug(
            db_session=db_session, stock_slug=stock_slug
        )
    except Exception as e:
        logger.error(e)

    return {"data": article_data_rows}


@router.get("/api/article-data", response_model=ArticleDataResponse)
async def read_article_data():
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
