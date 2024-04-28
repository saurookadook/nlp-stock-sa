import logging
from fastapi import APIRouter
from sqlalchemy import select

from config import configure_logging
from db import db_session

configure_logging(app_name="nlp_ssa.api.routes.analysis_views")
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/analysis-views/test")
async def read_analysis_views():
    from models.analysis_view import AnalysisViewDB
    from models.user import UserFacade
    from models.sentiment_analysis import SentimentAnalysisDB

    user_facade = UserFacade(db_session=db_session)

    try:
        user = user_facade.get_one_by_username("ovalle15")
    except Exception as e:
        raise e

    analysis_views = (
        db_session.execute(
            select(AnalysisViewDB)
            .where(AnalysisViewDB.user_id == user.id)
            .order_by(AnalysisViewDB.source_group_id)
        )
        .scalars()
        .all()
    )

    source_group_ids = [av.source_group_id for av in analysis_views]
    sentiment_analyses = (
        db_session.execute(
            select(SentimentAnalysisDB)
            .where(SentimentAnalysisDB.source_group_id.in_(source_group_ids))
            .order_by(SentimentAnalysisDB.source_group_id)
        )
        .scalars()
        .all()
    )

    results = []

    for tuple_result in zip(analysis_views, sentiment_analyses):
        results.append(
            dict(analysis_view=tuple_result[0], sentiment_analysis=tuple_result[1])
        )

    return results
