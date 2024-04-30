import os

env_config = dict(
    csrf_secret=os.getenv("CSRF_SECRET", "TMP"),
    database_user=os.getenv("DATABASE_USER", "postgres"),
    database_password=os.getenv("DATABASE_PASSWORD", "example"),
    database_host=os.getenv("DATABASE_HOST", "database"),
    database_port=os.getenv("DATABASE_PORT", "5432"),
    database_name=os.getenv("DATABASE_NAME", "the_money_maker"),
    env=os.getenv("ENV", "test"),
    log_level=os.getenv("LOG_LEVEL", "DEBUG"),
    log_sql=os.getenv("LOG_SQL", False),
)

from .logging import configure_logging, is_prod
