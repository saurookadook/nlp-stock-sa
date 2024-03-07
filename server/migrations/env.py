from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

from db import Base
from models import *


config = dict(
    database_user="TMP",
    database_password="TMP",
    database_host="TMP",
    database_port="TMP",
    database_name="the_money_maker",
)

# config = context.config

fileConfig(context.config.config_file_name)

context.config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycorp2://{config['database_user']}:{config['database_password']}"
    f"@{config['database_host']}:{config['database_port']}/{config['database_name']}",
)


def run_migrations_in_offline_mode():

    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_in_online_mode():

    engine = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        echo=config.log_sql,
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_in_offline_mode()
else:
    run_migrations_in_online_mode()
