import logging
from fastapi import Request

from api.routes.auth.session.caching import (
    build_cache_key,
    get_user_session,
)
from config import env_vars
from config.logging import ExtendedLogger


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

    active_user_session = get_user_session(
        cache_key=build_cache_key(entity_key=user_session_key)
    )

    if active_user_session is not None:
        logger.log_debug_centered(
            " handle_user_session: active_user_session ", fill_char="!"
        )
        logger.log_debug_pretty(active_user_session)
        return active_user_session

    return None
