import arrow
import pytest
from sqlalchemy import select, and_
from uuid import UUID

from models.article_data.db import ArticleDataDB
from models.article_data.factories import ArticleDataFactory
from models.sentiment_analysis.factories import SentimentAnalysisFactory
from models.source import SourceDB
from models.source.factories import SourceFactory
from models.stock.factories import StockFactory


@pytest.fixture
def mock_sentiment_analysis(mock_db_session):
    sentiment_analysis_mock = SentimentAnalysisFactory()


def test_source_db(mock_db_session, mock_ntdof_article_data):
    mock_article_data = mock_ntdof_article_data[0]

    mock_source = SourceFactory(id=UUID("6147bd1a-3157-41f1-a169-54396a6aeca6"))
    mock_db_session.commit()

    mock_db_article_data = ArticleDataDB(**mock_article_data.model_dump())

    mock_db_article_data.data_source = SourceDB(**mock_source.model_dump())

    mock_db_session.add(mock_db_article_data)
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(SourceDB).where(
            SourceDB.association_id == mock_db_article_data.source_association_id
        )
    ).scalar_one()

    assert result.id == mock_source.id
