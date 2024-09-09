from models.sentiment_analysis import SentimentAnalysisFacade


def get_all_sentiment_analyses_by_stock_slug(db_session, stock_slug):
    sentiment_analyses_rows = SentimentAnalysisFacade(
        db_session=db_session
    ).get_all_by_stock_symbol(quote_stock_symbol=stock_slug)

    return sorted(
        sentiment_analyses_rows, key=lambda sa: sa.source.data.last_updated_date
    )
