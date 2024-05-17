from sqlalchemy import func, select
from sqlalchemy.orm import aliased

from api.routes.api.article_data.models import ArticleDataEntry, GroupedArticleData


def get_all_article_data(db_session):
    from models.article_data import ArticleDataDB

    subquery = (
        select(
            ArticleDataDB,
            func.row_number()
            .over(
                partition_by=ArticleDataDB.quote_stock_symbol,
                order_by=ArticleDataDB.updated_at.desc(),
            )
            .label("row_number"),
        )
        .select_from(ArticleDataDB)
        .subquery()
    )

    grouped_data_sq = aliased(ArticleDataDB, subquery)

    article_data_row_query = (
        select(grouped_data_sq)
        .where(subquery.c.row_number <= 5)
        .limit(30)
        .execution_options(yield_per=5)
    )

    grouped_article_data_rows = dict()

    for data_row in db_session.scalars(article_data_row_query):
        if data_row.quote_stock_symbol not in grouped_article_data_rows.keys():
            grouped_article_data_rows[data_row.quote_stock_symbol] = dict(
                quote_stock_symbol=data_row.quote_stock_symbol, article_data=[]
            )
        grouped_article_data_rows[data_row.quote_stock_symbol]["article_data"].append(
            ArticleDataEntry.model_validate(data_row)
        )

    return [GroupedArticleData(**val) for val in grouped_article_data_rows.values()]


def get_article_data_by_stock_slug(db_session, stock_slug):
    from models.article_data import ArticleDataFacade

    article_data_rows = ArticleDataFacade(
        db_session=db_session
    ).get_all_by_stock_symbol(stock_slug)

    return article_data_rows
