import arrow
import logging
from sqlalchemy import Dialect, create_engine, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.types import TypeDecorator
from typing import Any

logger = logging.getLogger(__name__)

# TODO: move this elsewhere lol
config = dict(
    database_user="TMP",
    database_password="TMP",
    database_host="TMP",
    database_port="TMP",
    database_name="TMP",
    log_sql="TMP",
)

engine = create_engine(
    f"postgresql+psycorp2://{config.database_user}:{config.database_password}"
    f"@{config.database_host}:{config.database_port}/{config.database_name}",
    echo=config.log_sql,
    max_overflow=30,
    connect_args={"options": "-c timezone=utc"},
    future=True,
)

Base = declarative_base()

Base.metadata.naming_conventions = {
    "ix": "ix_%(column_0_N_label)s",
    "uq": "%(table_name)s_%(column_0_N_name)s_key",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "%(table_name)s_%(column_0_N_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
)


class ArrowDateClass(TypeDecorator):
    """TODO :]

    Args:
        TypeDecorator : _description_
    """

    impl = TIMESTAMP

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
