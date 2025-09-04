import logging
import secrets
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_csrf_protect import CsrfProtect

# from jose import JWTError, jwt
from oauthlib.oauth2 import WebApplicationClient

from api.routes.auth.models.responses import LoginResponse, LogoutResponse
from config import env_vars
from config.logging import ExtendedLogger
from db import db_session
from models.user_session import UserSessionFacade

logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()

# TODO: START -----------------------------------------------------------------
# - all of this should maybe go into `api.routes.auth.github.dependencies`...?
oauth2_auth_code_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=env_vars.GITHUB_OAUTH_AUTH_URL,
    tokenUrl=env_vars.GITHUB_OAUTH_TOKEN_URL,
    # scopes=["read:user"],
)
github_client = WebApplicationClient(env_vars.GITHUB_OAUTH_CLIENT_ID)


def build_github_url(request: Request):
    request.state.github_oauth_state = secrets.token_urlsafe(16)

    github_url = github_client.prepare_request_uri(
        env_vars.GITHUB_OAUTH_AUTH_URL,
        redirect_uri="https://nlp-ssa.dev/api/auth/github-callback",
        scope=["read:user", "user:email"],
        # TODO: eventually need this lol
        # state=request.state.github_oauth_state,
        allow_signup="true",
    )

    logger.info(f"github_url: '{github_url}'")

    return github_url


# TODO: END -----------------------------------------------------------------


@router.get("/login", response_model=LoginResponse)
async def read_login(
    request: Request,
    github_url: str = Depends(build_github_url),
):

    return {"github_url": github_url}


@router.delete("/logout", response_model=LogoutResponse)
async def do_logout(
    request: Request,
    response: Response,
):
    logger.log_debug_centered(" do_logout ")
    logger.log_debug_pretty(request)
    # TODO: this might be a good dependency :]
    user_session_key = request.cookies.get(env_vars.AUTH_COOKIE_KEY)

    deleted_user_session = UserSessionFacade(
        db_session=db_session
    ).delete_one_by_cache_key(user_session_key)

    if not deleted_user_session:
        return {
            "message": "Logout unsuccessful. Are you sure that you're currently logged in?"
        }

    response.delete_cookie(key=env_vars.AUTH_COOKIE_KEY, domain=env_vars.BASE_DOMAIN)
    return {
        "message": "Logout successful",
    }
