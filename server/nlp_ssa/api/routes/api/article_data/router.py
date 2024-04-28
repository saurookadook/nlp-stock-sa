from fastapi import APIRouter
from sqlalchemy import select

from db import db_session

router = APIRouter()


@router.get("/api/article-data/{stock_slug}")
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

    return [ad_data.__dict__ for ad_data in article_data_rows]


@router.get("/api/article-data")
async def read_all_article_data():
    from models.article_data import ArticleDataDB

    all_article_data_rows = db_session.execute(select(ArticleDataDB)).scalars().all()

    return [ad_data.__dict__ for ad_data in all_article_data_rows]
