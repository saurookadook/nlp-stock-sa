import pytest

from models.analysis_view import AnalysisViewFacade


@pytest.fixture
def analysis_view_facade(mock_db_session):
    return AnalysisViewFacade(db_session=mock_db_session)
