import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from api.dependencies.user_session import handle_user_session
from api.routes.auth.session.models import UserSessionCacheValue
from config.logging import ExtendedLogger
from db import db_session


logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


@router.get("/api/analysis-views/test")
async def read_analysis_views(
    user_session: UserSessionCacheValue = Depends(handle_user_session),
):
    from models.analysis_view import AnalysisViewDB
    from models.user import UserFacade
    from models.sentiment_analysis import SentimentAnalysisDB

    # TODO: START -------------------------------------------------------------
    # - this could/should all probably go into a dependency
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current user not authorized to access this resource.",
        )

    user_facade = UserFacade(db_session=db_session)

    try:
        user = user_facade.get_one_by_session_id(user_session.user_session_id)
    except Exception as e:
        raise e
    # TODO: END ---------------------------------------------------------------

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

    # TODO: this almost certainly isn't going to work as intended lol
    for tuple_result in zip(analysis_views, sentiment_analyses):
        results.append(
            dict(analysis_view=tuple_result[0], sentiment_analysis=tuple_result[1])
        )

    return results
