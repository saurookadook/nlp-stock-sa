import arrow
import logging
import re
from pydantic import alias_generators
from sqlalchemy import Dialect, create_engine, TIMESTAMP
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, scoped_session
from sqlalchemy.types import TypeDecorator
from typing import Any
from uuid import UUID, uuid4

from config import env_config


logger = logging.getLogger(__file__)

engine = create_engine(
    f"postgresql+psycopg2://{env_config['database_user']}:{env_config['database_password']}"
    f"@{env_config['database_host']}:{env_config['database_port']}/{env_config['database_name']}",
    echo=env_config["log_sql"],
    max_overflow=30,
    connect_args={"options": "-c timezone=utc"},
    future=True,
)


@as_declarative()
class Base(object):

    @declared_attr
    def __tablename__(cls):
        # TODO: probably have to trim off the `_db` too...?
        db_suffix = re.compile(r"_db$", flags=re.IGNORECASE | re.MULTILINE)
        return alias_generators.to_snake(cls.__name__).replace(db_suffix, "")

    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4()
    )


Base.metadata.naming_conventions = {
    "ix": "ix_%(column_0_N_label)s",
    "uq": "%(table_name)s_%(column_0_N_name)s_key",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "%(table_name)s_%(column_0_N_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
)


class ArrowDateClass(TypeDecorator):
    """TODO :]

    Args:
        TypeDecorator : _description_
    """

    impl = TIMESTAMP
    cache_ok = False

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any | None:
        # return super().process_bind_param(value, dialect)
        if value is not None:
            return value.datetime

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        # return super().process_result_value(value, dialect)
        if value is not None:
            return arrow.get(value)


def ArrowDate(*args, **kwargs):
    """For use in SQLAlchemy models when defining columns"""

    if "timezone" not in kwargs:
        kwargs["timezone"] = True
    return ArrowDateClass(*args, **kwargs)


def db_session_dependency():
    """FastAPI dependency to get database session

    Yields:
        Session: open database session
    """
    session = db_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
