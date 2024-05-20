import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from uuid import uuid4

from api.routes.auth.session.caching import get_user_from_session_cache
from config import env_vars


logger = logging.getLogger(__file__)
router = APIRouter()


def is_user_authorized_dependency(
    request: Request, session_id: str = Depends(get_user_from_session_cache)
):
    if not session_id:
        return RedirectResponse(env_vars.BASE_APP_URL + "/login")

    return request


# @router.post("/create_session/{name}")
# async def create_session(name: str, response: Response):
#     session = uuid4()
