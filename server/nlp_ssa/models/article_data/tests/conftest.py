import pytest

from models.article_data import ArticleDataFacade


@pytest.fixture
def article_data_facade(mock_db_session):
    return ArticleDataFacade(db_session=mock_db_session)
