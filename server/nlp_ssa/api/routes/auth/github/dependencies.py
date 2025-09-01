import logging
import requests
import secrets
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from rich import inspect, pretty
from typing import Dict
from urllib import parse

from api.routes.auth.session.caching import (
    build_cache_key,
    safe_set_in_session_cache,
    get_or_set_user_session_cache,
)
from config import env_vars
from config.logging import ExtendedLogger
from constants import ONE_DAY_IN_SECONDS


logger: ExtendedLogger = logging.getLogger(__file__)


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
    #     'access_token': 'ghu_<shorter token>',
    #     'expires_in': 28800, # 8 hours in seconds
    #     'refresh_token': 'ghr_<big long token>',
    #     'refresh_token_expires_in': 15897600, # 6 months in seconds
    #     'token_type': 'bearer',
    #     'scope': ''
    # }

    if token := token_data.get("access_token"):
        print("-" * 160)
        pretty.pprint(
            {
                "name": "get_auth_info_from_github",
                "req_query_params": request.query_params,
                "token": token,
            },
            expand_all=True,
        )
        print("-" * 160, end="\n\n")
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
def create_or_update_user_session(
    request: Request,  # force formatting
):
    user_session_key = request.cookies.get(env_vars.AUTH_COOKIE_KEY)
    session_cookie_config = dict(
        key=env_vars.AUTH_COOKIE_KEY,
        value=user_session_key,
        max_age=ONE_DAY_IN_SECONDS,
        domain=env_vars.BASE_DOMAIN,
        httponly=True,
        # samesite='strict'
    )

    user_session_from_cache = get_or_set_user_session_cache(
        cache_key=build_cache_key(entity_key=user_session_key)
    )

    if user_session_from_cache:
        logger.debug(f"WOOOOO USER SESSION FROM CACHE!!!")
        logger.debug(inspect(user_session_from_cache))
        return session_cookie_config

    auth_info = get_auth_info_from_github(request)

    token_data = auth_info.get("token_data")
    user_info = auth_info.get("user_info")

    username = user_info.get("login")
    cookie_value = user_session_key or f"{username}:{secrets.token_urlsafe(17)}"
    session_cookie_config = dict(
        key=env_vars.AUTH_COOKIE_KEY,
        value=cookie_value,
        max_age=ONE_DAY_IN_SECONDS,
        domain=env_vars.BASE_DOMAIN,
        httponly=True,
        # samesite='strict'
    )

    updated = get_or_set_user_session_cache(
        cache_key=build_cache_key(entity_key=cookie_value),
        details=dict(cookie_config=session_cookie_config, token_data=token_data),
    )

    if not updated:
        logger.error(f" github_oauth_callback: updated - {updated}")
        return HTTPException(status_code=500, detail="cache miss :(")

    return session_cookie_config
