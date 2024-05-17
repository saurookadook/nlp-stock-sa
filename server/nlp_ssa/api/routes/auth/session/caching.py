import json
import logging
from fastapi import Request
from pymemcache import Client
from pymemcache.client.retrying import RetryingClient
from pymemcache.exceptions import MemcacheUnexpectedCloseError
from typing import Dict, Union

from config import env_vars

logger = logging.getLogger(__name__)

base_client = Client((env_vars.MEMCACHED_HOST, env_vars.MEMCACHED_PORT))
retry_client = RetryingClient(
    base_client,
    attempts=3,
    retry_delay=0.2,
    retry_for=[ConnectionResetError, MemcacheUnexpectedCloseError],
)

TTL_SECONDS = 600  # 60s * 10 = 10min


def build_cache_key(*, entity_id: str, entity_type: str = "session"):
    return f"{entity_type}:{entity_id}"


def safe_get_from_session_cache(key: str):
    logger.info(f"Attempting to retrieve value for '{key}' from session cache...")
    cached_value = retry_client.get(key)
    if not cached_value:
        logger.warning(f"No value found for '{key}' in session cache")
        return None

    try:
        return json.loads(cached_value.decode("utf-8"))
    except Exception as e:
        logger.warning(f"Encountered error deserializing cached value for '{key}'")
        logger.warning(e)
        return cached_value


def safe_update_in_session_cache(
    cache_key: str, details: Dict[str, Union[str, bool, int, float]]
):
    logger.info(
        f"Updating value for key '{cache_key}' in session cache with expiration TTL of '{TTL_SECONDS}'"
    )

    retry_client.set(cache_key, json.dumps(details).encode("utf-8"), expire=TTL_SECONDS)

    return details


def get_user_from_session_cache(request: Request):

    session_id = request.cookies.get(env_vars.AUTH_COOKIE_KEY)
    cache_key = build_cache_key(session_id)

    cache_value = safe_get_from_session_cache(cache_key)

    if not cache_value:
        cache_value = safe_update_in_session_cache(
            cache_key=cache_key, details=dict(session_id=session_id)
        )

    logger.info("=" * 100)
    logger.info(f" RETRIEVED CACHE VALUE FOR '{cache_key}' ")
    logger.info(cache_value)
    logger.info("=" * 100)
    return cache_value
