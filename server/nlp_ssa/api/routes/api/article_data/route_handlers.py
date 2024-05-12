from sqlalchemy import desc, select

from api.routes.api.article_data.models import ArticleDataEntry, GroupedArticleData


def get_all_article_data(db_session):
    from models.article_data import ArticleDataDB

    article_data_row_query = (
        select(ArticleDataDB)
        .group_by(ArticleDataDB.id, ArticleDataDB.quote_stock_symbol)
        .order_by(ArticleDataDB.quote_stock_symbol, desc(ArticleDataDB.updated_at))
        .limit(30)
        .execution_options(yield_per=10)
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
