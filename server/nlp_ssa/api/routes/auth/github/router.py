import logging
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from rich import inspect, pretty
from typing import Dict

from api.routes.auth.session.models import SessionCookieConfig
from api.routes.auth.github.dependencies import create_or_update_user_session
from config.logging import ExtendedLogger


logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


@router.get("/github-callback")
async def github_oauth_callback(
    request: Request = None,
    session_cookie_config: SessionCookieConfig = Depends(create_or_update_user_session),
    # token: str = Depends(oauth2_auth_code_scheme),
):
    response = RedirectResponse("https://nlp-ssa.dev/app")
    response.set_cookie(**session_cookie_config.model_dump(mode="json"))

    logger.log_debug_centered(" github_oauth_callback: before end ", fill_char="!")
    return response
