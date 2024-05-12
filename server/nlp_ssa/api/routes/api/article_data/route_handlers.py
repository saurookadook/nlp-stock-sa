import arrow
from sqlalchemy import select

# from models.article_data import ArticleDataDB, ArticleDataFacade


def get_all_article_data(db_session):
    from models.article_data import ArticleDataDB

    all_article_data_rows = (
        db_session.execute(select(ArticleDataDB).limit(30)).scalars().all()
    )

    return all_article_data_rows


def get_article_data_by_stock_slug(db_session, stock_slug):
    from models.article_data import ArticleDataFacade

    article_data_rows = ArticleDataFacade(
        db_session=db_session
    ).get_all_by_stock_symbol(stock_slug)

    return article_data_rows
