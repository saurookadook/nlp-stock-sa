import os
from pathlib import Path
from dotenv import dotenv_values  # new


# BASE_DIR = Path(__file__).resolve().parent.parent

# ENV_FILE = f"{str(Path(BASE_DIR))}/.env"
# myvars = dotenv_values(ENV_FILE)


GITHUB_OAUTH_CLIENT_ID = os.getenv("GITHUB_OAUTH_CLIENT_ID", default="")
GITHUB_OAUTH_SECRET = os.getenv("GITHUB_OAUTH_CLIENT_SECRET", default="")
GITHUB_OAUTH_CALLBACK_URL = os.getenv("GITHUB_OAUTH_CALLBACK_URL", default="")
GITHUB_OAUTH_SCOPES = []

env_config = dict(
    csrf_secret=os.getenv("CSRF_SECRET", "TMP"),
    database_user=os.getenv("DATABASE_USER", "postgres"),
    database_password=os.getenv("DATABASE_PASSWORD", "example"),
    database_host=os.getenv("DATABASE_HOST", "database"),
    database_port=os.getenv("DATABASE_PORT", "5432"),
    database_name=os.getenv("DATABASE_NAME", "the_money_maker"),
    env=os.getenv("ENV", "dev"),
    log_level=os.getenv("LOG_LEVEL", "DEBUG"),
    log_sql=os.getenv("LOG_SQL", False),
)

from .logging import configure_logging, is_prod
