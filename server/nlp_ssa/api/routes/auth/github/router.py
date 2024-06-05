import logging
import requests
import secrets
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import Dict
from urllib import parse

from pprint import pprint as prettyprint
from rich import inspect

# TODO: remove
from api.routes.auth.session.caching import (
    build_cache_key,
    safe_update_in_session_cache,
)
from config import env_vars
from config.logging import ExtendedLogger
from constants import ONE_DAY_IN_SECONDS
from models.user import User


logger: ExtendedLogger = logging.getLogger(__file__)
router = APIRouter()


def exchange_code_for_token(code):
    params = {
        "client_id": env_vars.GITHUB_OAUTH_CLIENT_ID,
        "client_secret": env_vars.GITHUB_OAUTH_CLIENT_SECRET,
        "code": code,
    }

    request_url = f"{env_vars.GITHUB_OAUTH_TOKEN_URL}?{parse.urlencode(params)}"
    response = requests.post(
        request_url,
        headers={"Accept": "application/json"},
    )

    try:
        token_data = response.json()
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Nope :["
        )

    return token_data


def get_auth_info_from_github(request: Request):
    token_data = exchange_code_for_token(request.query_params.get("code"))

    # example 'token_data' shape:
    # {
    #     'access_token': 'ghu_KC1E4TezUCrudeKxQm7tMu7Nsfq8k21JjQ0r',
    #     'expires_in': 28800,
    #     'refresh_token':
    #     'ghr_5zHgUi6Z6Vz9NwsjqbY70SRfFe1bYnjtPoucXMtrcJujfyU9mrV6hFSO'+20,
    #     'refresh_token_expires_in': 15897600,
    #     'token_type': 'bearer',
    #     'scope': ''
    # }

    if token := token_data.get("access_token"):
        print("=" * 100)
        print(f"token: {token}")
        print("=" * 100, end="\n\n")
    else:
        raise Exception("get_user_info_from_github: no token!!! :o")

    # "https://api.github.com/user/emails"
    github_api_response = requests.get(
        "https://api.github.com/user",
        json={"access_token": token},
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    try:
        return dict(
            token_data=token_data,
            user_info=github_api_response.json(),
        )
    except Exception as e:
        logger.error("ERROR encountered in 'get_user_info_from_github'")
        raise e


# TODO: better name...?
def handle_user_session_dependency(
    request: Request, auth_info: Dict = Depends(get_auth_info_from_github)
):
    token_data = auth_info.get("token_data")
    user_info = auth_info.get("user_info")

    username = user_info.get("login")
    session_cookie_config = dict(
        key=env_vars.AUTH_COOKIE_KEY,
        value=f"{username}:{secrets.token_urlsafe(17)}",
        max_age=ONE_DAY_IN_SECONDS,
        domain=env_vars.BASE_DOMAIN,
        httponly=True,
        # samesite='strict'
    )

    updated = safe_update_in_session_cache(
        cache_key=build_cache_key(entity_id=username),
        details=dict(cookie_config=session_cookie_config, token_data=token_data),
    )

    if not updated:
        logger.error(f" github_oauth_callback: updated - {updated}")
        return HTTPException(status_code=500, detail="cache miss :(")

    return session_cookie_config


@router.get("/github-callback")
async def github_oauth_callback(
    fast_api_request: Request = None,
    session_cookie_config: Dict = Depends(handle_user_session_dependency),
    # token: str = Depends(oauth2_auth_code_scheme),
):
    response = RedirectResponse("https://nlp-ssa.dev/app")
    response.set_cookie(**session_cookie_config)

    return response
