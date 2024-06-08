import arrow
import pytest
from sqlalchemy import select, and_
from uuid import UUID

from models.article_data.factories import ArticleDataFactory
from models.source import SourceDB

# from models.source.factories import SourceFactory
from models.sentiment_analysis.factories import SentimentAnalysisFactory


@pytest.fixture
def mock_article_data():
    return ArticleDataFactory()


def test_source_db(mock_db_session):
    assert "Implement me!" == False
