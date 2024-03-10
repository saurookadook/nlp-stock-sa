import arrow
import logging
from sqlalchemy import Dialect, create_engine, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.types import TypeDecorator
from typing import Any

logger = logging.getLogger(__name__)

# TODO: move this elsewhere lol
env_config = dict(
    database_user="postgres",
    database_password="example",
    database_host="database",
    database_port="5432",
    database_name="the_money_maker",
    log_sql=True,
)

engine = create_engine(
    f"postgresql+psycopg2://{env_config['database_user']}:{env_config['database_password']}"
    # f"postgresql://{env_config['database_user']}:{env_config['database_password']}"
    f"@{env_config['database_host']}:{env_config['database_port']}/{env_config['database_name']}",
    echo=env_config["log_sql"],
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


def db_session():
    """FastAPI dependency to get database session

    Yields:
        Session: open database session
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
