import logging
import secrets
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_csrf_protect import CsrfProtect

# from jose import JWTError, jwt
from oauthlib.oauth2 import WebApplicationClient
from typing import Annotated

from api.routes.auth.login.models import LoginResponse
from config import env_vars
from db import db_session
from models.user import User, UserFacade


logger = logging.getLogger(__file__)
router = APIRouter()


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


@router.get("/login", response_model=LoginResponse)
async def read_login(
    request: Request = None,
    csrf_protect: CsrfProtect = Depends(),
    github_url: str = Depends(build_github_url),
):
    # await csrf_protect.validate_csrf(request)

    return {"github_url": github_url}


# TODO: these might get removed :)
def user_facade_dependency():
    return UserFacade(db_session=db_session)


def fake_decode_token(token):
    return User(
        username=token + "_fakedecoded",
        email="maskiella@gmail.com",
        first_name="Andy",
        last_name="Maskiell",
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_auth_code_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
