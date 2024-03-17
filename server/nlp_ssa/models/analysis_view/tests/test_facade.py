import pytest

from models.analysis_view import AnalysisView, AnalysisViewFacade, AnalysisViewFactory


@pytest.fixture
def analysis_view_facade(mock_db_session):
    return AnalysisViewFacade(db_session=mock_db_session)


def test_get_one_by_id(mock_db_session, analysis_view_facade):
    mock_analysis_view = AnalysisViewFactory()
    mock_db_session.commit()

    result = analysis_view_facade.get_one_by_id(id=mock_analysis_view.id)

    assert result == AnalysisView.model_validate(mock_analysis_view)


def test_get_one_by_id_no_result(analysis_view_facade):
    with pytest.raises(AnalysisViewFacade.NoResultFound):
        analysis_view_facade.get_one_by_id(id="ba379b11-6c65-4cf9-af09-43c5ae41e979")
