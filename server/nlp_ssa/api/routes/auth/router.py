import logging
import secrets
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_csrf_protect import CsrfProtect

# from jose import JWTError, jwt
from oauthlib.oauth2 import WebApplicationClient

from api.routes.auth.models.responses import LoginResponse, LogoutResponse
from config import env_vars

logger = logging.getLogger(__file__)
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
async def read_login(
    request: Request,
):
    pass
