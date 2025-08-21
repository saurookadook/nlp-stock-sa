from models.sentiment_analysis import SentimentAnalysisFacade


def filter_func(sa_row):
    return (
        sa_row.source.data is not None
        and sa_row.source.data.last_updated_date is not None
    )


def get_all_sentiment_analyses_by_stock_slug(db_session, stock_slug):
    sentiment_analyses_rows = SentimentAnalysisFacade(
        db_session=db_session
    ).get_all_by_stock_symbol(quote_stock_symbol=stock_slug)

    filtered_sentiment_analyses_rows = list(
        filter(filter_func, sentiment_analyses_rows)
    )

    return sorted(
        filtered_sentiment_analyses_rows,
        key=lambda sa: sa.source.data.last_updated_date,
    )
