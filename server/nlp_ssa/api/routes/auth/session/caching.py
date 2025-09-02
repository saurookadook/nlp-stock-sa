import json
import logging
from pymemcache import Client
from pymemcache.client.retrying import RetryingClient
from pymemcache.exceptions import MemcacheUnexpectedCloseError
from rich import inspect, pretty
from sqlalchemy.orm import Session, scoped_session
from typing import Dict, Union
from uuid import uuid4

from api.routes.auth.session.models import UserSessionCacheDetails
from config import env_vars
from config.logging import ExtendedLogger
from constants import AuthProviderEnum
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


def get_or_set_user_session(
    *,
    auth_provider: AuthProviderEnum = AuthProviderEnum.GITHUB,
    cache_key: str,
    details: UserSessionCacheDetails = None,
):
    logger.debug(" get_or_set_user_session ".center(120, "="))
    pretty.pprint(
        {"auth_provider": auth_provider, "cache_key": cache_key, "details": details},
        expand_all=True,
    )

    user_session = get_user_session(cache_key, auth_provider)

    logger.debug(" get_or_set_user_session: user_session ".center(120, "?"))
    pretty.pprint(user_session, expand_all=True)

    if not user_session and details is not None:
        user_session = safe_set_in_session_cache(
            auth_provider=auth_provider, cache_key=cache_key, details=details
        )

    logger.debug("=" * 100)
    logger.debug(f" RETRIEVED CACHE VALUE FOR '{cache_key}' ")
    pretty.pprint(user_session, expand_all=True)
    logger.debug("=" * 100)
    return user_session


def get_user_session(cache_key: str, auth_provider: AuthProviderEnum):
    cache_value = safe_get_from_session_cache(cache_key=cache_key)

    if cache_value:
        return cache_value

    _, entity_key = parse_cache_key(cache_key)
    username = entity_key.split(":")[0]

    logger.log_debug_centered(" get_user_session ")
    logger.debug(f"{'-'*12} username: '{username}'")
    try:
        local_db_session: scoped_session[Session] = db_session
        user = UserFacade(db_session=local_db_session).get_one_by_username(username)
        logger.debug(f"{'-' * 24} get_user_session: user")
        pretty.pprint(user, expand_all=True)
        user_session = UserSessionFacade(
            db_session=local_db_session
        ).get_first_by_user_id_and_auth_provider(
            user_id=user.id, auth_provider=auth_provider
        )
        logger.debug(f"{'-' * 24} get_user_session: user_session")
        pretty.pprint(user_session, expand_all=True)

        return user_session
    except Exception as e:
        logger.debug(e)
        return None


def safe_get_from_session_cache(*, cache_key: str):
    # logger.debug(" safe_get_from_session_cache ".center(120, "="))
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
    auth_provider: AuthProviderEnum = AuthProviderEnum.GITHUB,
    cache_key: str,
    details: UserSessionCacheDetails,  # TODO: make this type better
):
    logger.log_debug_centered(" upsert_user_session ")
    logger.debug(f"{'-' * 24} upsert_user_session")

    _, entity_key = parse_cache_key(cache_key)
    username = entity_key.split(":")[0]

    user_session = None

    try:
        local_db_session: scoped_session[Session] = db_session
        user = UserFacade(db_session=local_db_session).get_one_by_username(username)
        logger.debug(f"{'-' * 24} get_user_session: user")
        pretty.pprint(user, expand_all=True)

        user_session = UserSessionFacade(db_session=local_db_session).create_or_update(
            payload=dict(
                id=uuid4(),
                user_id=user.id,
                access_token=details.token_data.access_token,
                auth_provider=auth_provider,
                expires_in=details.token_data.expires_in,
                refresh_token=details.token_data.refresh_token,
                refresh_token_expires_in=details.token_data.refresh_token_expires_in,
                token_type=details.token_data.token_type,
            )
        )
        logger.debug(f"{'-' * 24} get_user_session: user_session")
        pretty.pprint(user_session, expand_all=True)
        local_db_session.commit()
    except Exception as e:
        logger.debug(e)
        raise e

    cache_details = safe_set_in_session_cache(
        auth_provider=auth_provider, cache_key=cache_key, details=details
    )

    # TODO: this feels messy...
    return cache_details or user_session


def safe_set_in_session_cache(
    *,
    auth_provider: AuthProviderEnum = AuthProviderEnum.GITHUB,
    cache_key: str,
    details: UserSessionCacheDetails,  # TODO: make this type better
):
    logger.debug(f"{'-' * 24} safe_set_in_session_cache")
    logger.info(
        f"Updating value for key '{cache_key}' in session cache with expiration TTL of '{TTL_SECONDS}'"
    )

    cache_result = retry_client.set(
        cache_key,
        # TODO: include auth_provider in here...?
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
