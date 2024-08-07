import logging
from fastapi import APIRouter, HTTPException

from config.logging import ExtendedLogger, configure_logging
from db import db_session

configure_logging(app_name=__file__)
logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


@router.get("/api/users/{username}")
async def read_users_test(username: str):
    from models.user import UserFacade

    user_facade = UserFacade(db_session=db_session)

    try:
        logger.log_warn_centered(f" getting user ")
        user = user_facade.get_one_by_username(username=username)
    except UserFacade.NoResultFound:
        raise HTTPException(
            status_code=404, detail=f"Could not find user with username '{username}'"
        )

    return {"user": user}
