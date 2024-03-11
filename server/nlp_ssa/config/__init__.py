env_config = dict(
    csrf_secret="TMP",
    database_user="postgres",
    database_password="example",
    database_host="database",
    database_port="5432",
    database_name="the_money_maker",
    env="test",
    log_level="DEBUG",
    log_sql=True,
)

from .logging import configure_logging, is_prod
