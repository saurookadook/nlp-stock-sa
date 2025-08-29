import logging
from fastapi import Request
from rich import inspect, pretty

from api.routes.auth.session.caching import (
    build_cache_key,
    get_or_set_user_session_cache,
)
from config import env_vars
from config.logging import ExtendedLogger
from constants import ONE_DAY_IN_SECONDS


logger: ExtendedLogger = logging.getLogger(__file__)


# TODO: Better name...?
async def handle_user_session(request: Request) -> dict | None:
    """Dependency to handle getting user session from cookie value.

    Args:
        `request`: The FastAPI request object.

    Returns:
        `dict | None`: The user session data. Returns `None` if not found.
    """
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

    if not user_session_from_cache:
        return None

    # TODO: get `user_session` record with ID from cache
    logger.debug(f"WOOOOO USER SESSION FROM CACHE!!!")
    logger.debug(inspect(user_session_from_cache))
    return session_cookie_config
