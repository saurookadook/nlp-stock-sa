import arrow
import pytest
from sqlalchemy import select, and_
from uuid import UUID

from models.analysis_view import AnalysisViewDB
from models.analysis_view.factories import AnalysisViewFactory


mock_source_group_id = UUID("16ec77ca-7dd0-483d-be53-f625618d66ab")


@pytest.fixture
def expected_analysis_view_dict():
    return dict(
        id=UUID("4c26429c-c8e8-4fc6-9b39-357d3e5e7dd6"),
        source_group_id=mock_source_group_id,
        # owner_id=mock_user_id,
    )


def test_analysis_view_db_no_user(mock_db_session, expected_analysis_view_dict):
    analysis_view = AnalysisViewFactory(**expected_analysis_view_dict, user=None)
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(AnalysisViewDB).where(
            and_(
                AnalysisViewDB.id == analysis_view.id,
                AnalysisViewDB.source_group_id == mock_source_group_id,
            )
        )
    ).scalar_one()

    assert result.id == expected_analysis_view_dict["id"]
    assert result.source_group_id == expected_analysis_view_dict["source_group_id"]
    # assert result.owner_id == expected_analysis_view_dict["owner_id"]
    assert result.user_id is None
    assert result.created_at == arrow.get(2024, 4, 1).to("utc")
    assert result.updated_at == arrow.get(2024, 4, 1).to("utc")


def test_analysis_view_db_with_user(
    mock_db_session, mock_user, expected_analysis_view_dict
):
    analysis_view = AnalysisViewFactory(**expected_analysis_view_dict)
    analysis_view.user = mock_user
    mock_db_session.commit()

    result = mock_db_session.execute(
        select(AnalysisViewDB).where(
            and_(
                AnalysisViewDB.id == analysis_view.id,
                AnalysisViewDB.user_id == mock_user.id,
            )
        )
    ).scalar_one()

    assert result.id == expected_analysis_view_dict["id"]
    assert result.source_group_id == expected_analysis_view_dict["source_group_id"]
    # assert result.owner_id == expected_analysis_view_dict["owner_id"]
    assert result.user_id == mock_user.id
    assert result.created_at == arrow.get(2024, 4, 1).to("utc")
    assert result.updated_at == arrow.get(2024, 4, 1).to("utc")
