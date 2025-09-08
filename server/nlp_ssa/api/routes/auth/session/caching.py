import arrow
import json
import logging
from pymemcache import Client
from pymemcache.client.retrying import RetryingClient
from pymemcache.exceptions import MemcacheUnexpectedCloseError
from sqlalchemy.orm import Session, scoped_session
from uuid import uuid4

from api.routes.auth.session.models import (
    SessionCookieConfig,
    UserSessionCacheDetails,
    UserSessionCacheValue,
)
from config import env_vars
from config.logging import ExtendedLogger
from constants import ONE_DAY_IN_SECONDS
from db import db_session
from models.user import UserFacade
from models.user_session import UserSessionFacade


logger: ExtendedLogger = logging.getLogger(__file__)
logger.setLevel(logging.WARNING)  # to shush the logs while not debugging

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


def get_user_session(cache_key: str) -> UserSessionCacheValue | None:
    logger.log_debug_centered(" get_user_session: START ", fill_char="=")
    cache_value = safe_get_from_session_cache(cache_key=cache_key)

    if cache_value:
        logger.log_debug_centered(" get_user_session: END (w/ cached) ", fill_char="=")
        return cache_value

    _, entity_key = parse_cache_key(cache_key)
    username = entity_key.split(":")[0]

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

        cache_value = UserSessionCacheValue(
            auth_provider=user_session.auth_provider,
            cookie_config=SessionCookieConfig(
                key=env_vars.AUTH_COOKIE_KEY,
                value=cache_key,
                max_age=ONE_DAY_IN_SECONDS,
                domain=env_vars.BASE_DOMAIN,
            ),
            # TODO: this value should come from the user_session
            expires_at=get_expiration_date_in_seconds(user_session.expires_in),
            user_session_id=user_session.id,
        )

        safe_set_in_session_cache(
            cache_key=cache_key,
            cache_value=cache_value,
        )
    except Exception as e:
        logger.debug(e)

    logger.log_debug_centered(" get_user_session: END (w/ DB result) ", fill_char="=")
    return cache_value


def safe_get_from_session_cache(*, cache_key: str) -> UserSessionCacheValue | None:
    logger.log_debug_centered(" safe_get_from_session_cache ", fill_char="=")
    logger.debug(
        f"Attempting to retrieve value for '{cache_key}' from session cache..."
    )

    cached_value = retry_client.get(cache_key)
    logger.debug(f"{'-' * 24} response from memcached ")
    logger.debug(cached_value)

    if not cached_value:
        logger.debug(f"No value found for '{cache_key}' in session cache")
        return None

    try:
        json_value = json.loads(cached_value.decode("utf-8"))
        logger.debug(f"{'-' * 24} safe_get_from_session_cache: json_value")
        logger.log_debug_pretty(json_value)
        deserialized_value = UserSessionCacheValue.model_validate(
            dict(
                auth_provider=json_value["auth_provider"],
                cookie_config=json_value["cookie_config"],
                expires_at=json_value["expires_at"],
                user_session_id=json_value["user_session_id"],
            )
        )

        return deserialized_value
    except Exception as e:
        logger.warning(
            f"Encountered error deserializing cached value for '{cache_key}'"
        )
        logger.warning(e)
        raise e


def upsert_user_session(
    *,
    cache_key: str,
    details: UserSessionCacheDetails,
) -> UserSessionCacheValue:
    logger.log_debug_centered(" upsert_user_session: START ", fill_char="=")

    _, entity_key = parse_cache_key(cache_key)
    username = entity_key.split(":")[0]

    cache_value = None

    # TODO: this whole try/except block smells a bit...
    try:
        local_db_session: scoped_session[Session] = db_session

        user = UserFacade(db_session=local_db_session).get_one_by_username(username)
        logger.debug(f"{'-' * 24} upsert_user_session: user")
        logger.log_debug_pretty(user)

        user_session = UserSessionFacade(db_session=local_db_session).create_or_update(
            payload=dict(
                id=uuid4(),
                cache_key=entity_key,  # this was poorly named :[
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

        cache_value = UserSessionCacheValue(
            auth_provider=details.auth_provider,
            cookie_config=details.cookie_config,
            # TODO: this value should come from the user_session
            expires_at=get_expiration_date_in_seconds(details.token_data.expires_in),
            user_session_id=user_session.id,
        )

        safe_set_in_session_cache(
            cache_key=cache_key,
            cache_value=cache_value,
        )
    except Exception as e:
        logger.debug(e)
        raise e

    logger.log_debug_centered(" upsert_user_session: END ", fill_char="=")
    return cache_value


def safe_set_in_session_cache(
    *,
    cache_key: str,
    cache_value: UserSessionCacheValue,
) -> UserSessionCacheValue | None:
    logger.debug(f"{'-' * 24} safe_set_in_session_cache")
    logger.info(
        f"Updating value for key '{cache_key}' in session cache with expiration TTL of '{TTL_SECONDS}'"
    )

    cache_result = retry_client.set(
        cache_key,
        json.dumps(cache_value.model_dump(mode="json")).encode("utf-8"),
        expire=TTL_SECONDS,
    )

    if cache_result:
        return cache_value
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


def get_expiration_date_in_seconds(expires_in: int):
    return arrow.now().int_timestamp + expires_in
