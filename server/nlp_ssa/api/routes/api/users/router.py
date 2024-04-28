import logging
from fastapi import APIRouter, HTTPException

from config import configure_logging
from db import db_session

configure_logging(app_name="nlp_ssa.api.routes.users")
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/users/{username}")
async def read_users_test(username: str):
    from models.user import UserFacade

    user_facade = UserFacade(db_session=db_session)

    try:
        logger.warning(f"{'='*40} getting user {'='*40}")
        user = user_facade.get_one_by_username(username=username)
    except UserFacade.NoResultFound:
        raise HTTPException(
            status_code=404, detail=f"Could not find user with username '{username}'"
        )

    return {"user": user}
