from api.routes.api.article_data.models import GroupedArticleData
from api.routes.api.article_data.route_handlers import (
    get_all_article_data,
    get_article_data_by_stock_slug,
)
from models.article_data import ArticleData
from models.article_data.factories import ArticleDataFactory
from models.stock.factories import StockFactory


def test_get_all_article_data_one_stock(
    mock_db_session, mock_stocks, mock_ntdof_article_data
):
    ntdof_stock, _ = mock_stocks

    results = get_all_article_data(db_session=mock_db_session)

    ntdof_first_five = mock_ntdof_article_data[:5]
    expected = [
        GroupedArticleData(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            article_data=ntdof_first_five,
        )
    ]

    assert results == expected


def test_get_all_article_data_multiple_stocks(
    mock_db_session, mock_stocks, mock_ntdof_article_data, mock_tsla_article_data
):
    ntdof_stock, tsla_stock = mock_stocks

    results = get_all_article_data(db_session=mock_db_session)

    ntdof_first_five = mock_ntdof_article_data[:5]
    tsla_first_five = mock_tsla_article_data[:5]

    expected = [
        GroupedArticleData(
            quote_stock_symbol=ntdof_stock.quote_stock_symbol,
            article_data=ntdof_first_five,
        ),
        GroupedArticleData(
            quote_stock_symbol=tsla_stock.quote_stock_symbol,
            article_data=tsla_first_five,
        ),
    ]

    for i, result_group in enumerate(results):
        expected_group = expected[i]
        assert result_group.quote_stock_symbol == expected_group.quote_stock_symbol

        expected_article_data_for_group = expected_group.article_data
        for j, ad_result in enumerate(result_group.article_data):
            assert ad_result == expected_article_data_for_group[j]


def test_get_all_article_data_no_results(mock_db_session):
    results = get_all_article_data(db_session=mock_db_session)

    assert results == []


def test_get_article_data_by_stock_slug(mock_db_session):
    only_stock = StockFactory(quote_stock_symbol="ONLY")
    mock_db_session.commit()
    only_article_data = ArticleDataFactory(
        quote_stock_symbol=only_stock.quote_stock_symbol
    )
    mock_db_session.commit()

    results = get_article_data_by_stock_slug(
        db_session=mock_db_session, stock_slug=only_stock.quote_stock_symbol
    )

    expected = [ArticleData.model_validate(only_article_data)]

    assert results == expected


def test_get_article_data_by_stock_slug_multiple_results(
    mock_db_session, mock_stocks, mock_tsla_article_data
):
    _, tsla_stock = mock_stocks

    results = get_article_data_by_stock_slug(
        db_session=mock_db_session, stock_slug=tsla_stock.quote_stock_symbol
    )

    assert results == mock_tsla_article_data


def test_get_article_data_by_stock_slug_no_results(mock_db_session):
    nope_stock = StockFactory(quote_stock_symbol="NOPE")
    mock_db_session.commit()

    results = get_article_data_by_stock_slug(
        db_session=mock_db_session, stock_slug=nope_stock.quote_stock_symbol
    )

    assert results == []
