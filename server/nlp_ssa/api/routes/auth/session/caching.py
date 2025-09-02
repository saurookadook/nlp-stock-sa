import json
import logging
from pymemcache import Client
from pymemcache.client.retrying import RetryingClient
from pymemcache.exceptions import MemcacheUnexpectedCloseError
from sqlalchemy.orm import Session, scoped_session
from uuid import uuid4

from api.routes.auth.session.models import (
    SessionCookieConfig,
    TokenData,
    UserSessionCacheDetails,
)
from config import env_vars
from config.logging import ExtendedLogger
from constants import ONE_DAY_IN_SECONDS
from db import db_session
from models.user import UserFacade
from models.user_session import UserSessionFacade


logger: ExtendedLogger = logging.getLogger(__file__)

base_client = Client(
    (env_vars.MEMCACHED_HOST, env_vars.MEMCACHED_PORT),
    connect_timeout=0.25,
    timeout=0.25,
)
retry_client = RetryingClient(
    base_client,
    attempts=3,
    retry_delay=0.2,
    retry_for=[ConnectionResetError, MemcacheUnexpectedCloseError],
)

TTL_SECONDS = 600  # 60s * 10 = 10min


def get_user_session(cache_key: str):
    logger.log_debug_centered(" get_user_session: START ", fill_char="=")
    cache_value = safe_get_from_session_cache(cache_key=cache_key)

    if cache_value:
        logger.log_debug_centered(" get_user_session: END (w/ cached) ", fill_char="=")
        return cache_value

    _, entity_key = parse_cache_key(cache_key)
    username = entity_key.split(":")[0]

    user_session = None

    logger.log_debug_centered(" get_user_session ")
    logger.debug(f"{'-'*12} username: '{username}'")
    try:
        local_db_session: scoped_session[Session] = db_session

        user = UserFacade(db_session=local_db_session).get_one_by_username(username)
        logger.debug(f"{'-' * 24} get_user_session: user")
        logger.log_debug_pretty(user)

        user_session = UserSessionFacade(
            db_session=local_db_session
        ).get_one_by_cache_key(cache_key)
        logger.debug(f"{'-' * 24} get_user_session: user_session")
        logger.log_debug_pretty(user_session)

        safe_set_in_session_cache(
            cache_key=cache_key,
            details=UserSessionCacheDetails(
                auth_provider=user_session.auth_provider,
                cookie_config=SessionCookieConfig(
                    key=env_vars.AUTH_COOKIE_KEY,
                    value=cache_key,
                    max_age=ONE_DAY_IN_SECONDS,
                    domain=env_vars.BASE_DOMAIN,
                ),
                token_data=TokenData(
                    access_token=user_session.access_token,
                    expires_in=user_session.expires_in,
                    refresh_token=user_session.refresh_token,
                    refresh_token_expires_in=user_session.refresh_token_expires_in,
                    token_type=user_session.token_type,
                ),
            ),
        )
    except Exception as e:
        logger.debug(e)

    logger.log_debug_centered(" get_user_session: END (w/ DB result) ", fill_char="=")
    return user_session


def safe_get_from_session_cache(*, cache_key: str):
    logger.debug(f"{'-' * 24} safe_get_from_session_cache")
    logger.debug(
        f"Attempting to retrieve value for '{cache_key}' from session cache..."
    )

    cached_value = retry_client.get(cache_key)
    logger.debug(" response from memcached ".center(120, "="))
    logger.debug(cached_value)

    if not cached_value:
        logger.debug(f"No value found for '{cache_key}' in session cache")
        return None

    try:
        return json.loads(cached_value.decode("utf-8"))
    except Exception as e:
        logger.warning(
            f"Encountered error deserializing cached value for '{cache_key}'"
        )
        logger.warning(e)
        return cached_value


def upsert_user_session(
    *,
    cache_key: str,
    details: UserSessionCacheDetails,
):
    logger.log_debug_centered(" upsert_user_session: START ", fill_char="=")

    _, entity_key = parse_cache_key(cache_key)
    username = entity_key.split(":")[0]

    user_session = None

    try:
        local_db_session: scoped_session[Session] = db_session

        user = UserFacade(db_session=local_db_session).get_one_by_username(username)
        logger.debug(f"{'-' * 24} upsert_user_session: user")
        logger.log_debug_pretty(user)

        user_session = UserSessionFacade(db_session=local_db_session).create_or_update(
            payload=dict(
                id=uuid4(),
                cache_key=cache_key,
                user_id=user.id,
                access_token=details.token_data.access_token,
                auth_provider=details.auth_provider,
                expires_in=details.token_data.expires_in,
                refresh_token=details.token_data.refresh_token,
                refresh_token_expires_in=details.token_data.refresh_token_expires_in,
                token_type=details.token_data.token_type,
            )
        )
        logger.debug(f"{'-' * 24} upsert_user_session: user_session")
        logger.log_debug_pretty(user_session)

        local_db_session.commit()
    except Exception as e:
        logger.debug(e)
        raise e

    cache_details = safe_set_in_session_cache(
        auth_provider=details.auth_provider, cache_key=cache_key, details=details
    )

    logger.log_debug_centered(" upsert_user_session: END ", fill_char="=")
    # TODO: this feels messy...
    return cache_details or user_session


def safe_set_in_session_cache(
    *,
    cache_key: str,
    details: UserSessionCacheDetails,
):
    logger.debug(f"{'-' * 24} safe_set_in_session_cache")
    logger.info(
        f"Updating value for key '{cache_key}' in session cache with expiration TTL of '{TTL_SECONDS}'"
    )

    cache_result = retry_client.set(
        cache_key,
        # TODO:
        # - should the stored value just be the user_session ID and details.cookie_config?
        json.dumps(details.model_dump(mode="json")).encode("utf-8"),
        expire=TTL_SECONDS,
    )

    if cache_result:
        return details
    else:
        logger.warning("safe_set_in_session_cache: cache miss!!! :o")
        return None


# TODO: is the entity_type overkill...?
def build_cache_key(*, entity_key: str, entity_type: str = "session"):
    # TODO: maybe the entity_type could instead be some hashed value in an env variable?
    return f"{entity_type}|{entity_key}"


def parse_cache_key(cache_key: str):
    entity_type, entity_key = cache_key.split("|")

    return entity_type, entity_key


def debugging_wrapper(key):
    return safe_get_from_session_cache(cache_key=key)
