import arrow
import pytest
from sqlalchemy import select, and_
from uuid import UUID

from models.article_data.factories import ArticleDataFactory
from models.sentiment_analysis.factories import SentimentAnalysisFactory
from models.source import SourceDB
from models.source.factories import SourceFactory
from models.stock.factories import StockFactory


@pytest.fixture
def mock_stock(mock_db_session):
    ntdof_stock = StockFactory(quote_stock_symbol="NTDOF")


@pytest.fixture
def mock_sentiment_analysis(mock_db_session):
    sentiment_analysis_mock = SentimentAnalysisFactory()


def test_source_db(mock_db_session):
    assert "Implement me!" == False
