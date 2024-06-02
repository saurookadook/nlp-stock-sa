import logging
import requests
import secrets
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
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


async def get_user_info_from_github(token: str):
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

    print(" get_user_info_from_github: github_api_response ".center(100, "="))
    inspect(github_api_response, methods=True, sort=True)
    print("=" * 100, end="\n\n")

    try:
        return github_api_response.json()
    except Exception as e:
        logger.error("ERROR encountered in 'get_user_info_from_github'")
        raise e


@router.get("/github-callback")
async def github_oauth_callback(
    fast_api_request: Request = None,
    # token: str = Depends(oauth2_auth_code_scheme),
):
    token_data = exchange_code_for_token(fast_api_request.query_params.get("code"))

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
    prettyprint(token_data)

    if token := token_data.get("access_token"):
        print("=" * 100)
        print(f"token: {token}")
        print("=" * 100, end="\n\n")
        user_info = await get_user_info_from_github(token=token)
        prettyprint(user_info, indent=4, width=200)

    username = user_info.get("login")
    # cookie_value = f"{username}:{secrets.token_urlsafe(16)}"
    session_cookie_config = dict(
        key=env_vars.AUTH_COOKIE_KEY,
        value=f"{username}:{secrets.token_urlsafe(17)}",
        max_age=ONE_DAY_IN_SECONDS,
        domain=env_vars.BASE_DOMAIN,
        httponly=True,
        # samesite='strict'
    )
    # TODO: figure out why memcached server doesn't seem to be running
    await safe_update_in_session_cache(
        cache_key=build_cache_key(entity_id=username),
        details=dict(cookie_config=session_cookie_config, token_data=token_data),
    )

    response = RedirectResponse("https://nlp-ssa.dev/app")
    response.set_cookie(**session_cookie_config)

    return response
