import logging
from fastapi import APIRouter
from sqlalchemy import select

from api.routes.api.article_data.models import ArticleDataResponse
from config import configure_logging
from db import db_session

configure_logging(app_name="nlp_ssa.api.routes.article_data")
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/article-data/{stock_slug}", response_model=ArticleDataResponse)
async def read_article_data_by_slug(stock_slug: str):
    from models.article_data import ArticleDataDB

    article_data_rows = (
        db_session.execute(
            select(ArticleDataDB).where(
                ArticleDataDB.quote_stock_symbol == stock_slug.upper()
            )
        )
        .scalars()
        .all()
    )

    return {"data": article_data_rows}


@router.get("/api/article-data", response_model=ArticleDataResponse)
async def read_all_article_data():
    from models.article_data import ArticleDataDB

    all_article_data_rows = db_session.execute(select(ArticleDataDB)).scalars().all()

    return {"data": all_article_data_rows}
