from api.routes.api.sentiment_analyses.route_handlers import (
    get_all_sentiment_analyses_by_stock_slug,
)
from models.stock.factories import StockFactory


def test_get_all_sentiment_analyses_by_stock_slug(
    mock_db_session, mock_sentiment_analyses, mock_stocks
):
    ntdof_stock, _ = mock_stocks

    results = get_all_sentiment_analyses_by_stock_slug(
        db_session=mock_db_session, stock_slug=ntdof_stock.quote_stock_symbol
    )

    assert len(results) == len(mock_sentiment_analyses)
    assert results == mock_sentiment_analyses


def test_get_all_sentiment_analyses_by_stock_slug_no_results(mock_db_session):
    nope_stock = StockFactory(quote_stock_symbol="NOPE")
    mock_db_session.commit()

    results = get_all_sentiment_analyses_by_stock_slug(
        db_session=mock_db_session, stock_slug=nope_stock.quote_stock_symbol
    )

    assert results == []
