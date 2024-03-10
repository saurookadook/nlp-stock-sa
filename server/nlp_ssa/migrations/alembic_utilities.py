from alembic import op
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import MetaData
from typing import Dict, Iterable, Optional

from db import Base


def create_pg_enum(type_name: str, enum_options: Iterable[str]):
    alembic_connection = op.get_bind()

    enum = ENUM(
        *enum_options,
        name=type_name,
        metadata=Base.metadata,
    )
    enum.create(alembic_connection)
    return enum


def drop_pg_enum(type_name: str, enum_options: Iterable[str]):
    alembic_connection = op.get_bind()

    enum = ENUM(
        *enum_options,
        name=type_name,
        metadata=Base.metadata,
    )
    enum.drop(alembic_connection)


def alter_pg_enum(type_name: str, enum_column: any):
    model = enum_column.parent.entity

    table_name = model.__table__.name
    enum_column_name = enum_column.name
    type_name = type_name

    op.execute(
        (
            f"ALTER TABLE {table_name} "
            f"ALTER COLUMN {enum_column_name} TYPE {type_name} "
            f"USING ({enum_column_name}::text::{type_name});"
        )
    )


def modify_pg_enum(
    type_name,
    enum_column,
    replacement_type_options: Iterable[str],
    default: Optional[str] = None,
    replacement_map: Optional[Dict[str, str]] = None,
):

    alembic_connection = op.bind()

    model = enum_column.parent.entity

    table_name = model.__table__.name
    enum_column_name = enum_column.name
    new_type_name = f"{type_name}_new"

    new_enum = ENUM(
        *replacement_type_options,
        name=new_type_name,
        metadata=MetaData(bind=alembic_connection),
    )
    new_enum.create(alembic_connection)

    if default is not None:
        op.execute(
            f"ALTER TABLE {table_name} ALTER COLUMN {enum_column_name} DROP DEFAULT;"
        )

    if replacement_map:
        enum_map = "\n".join(
            f"WHEN '{old}' THEN '{new}'" for old, new in replacement_map.items()
        )
        using = f"""CASE {enum_column_name}::text
                {enum_map}
                ELSE {enum_column_name}::text
            END"""
    else:
        using = f"{enum_column_name}::text"

    op.execute(
        (
            f"ALTER TABLE {table_name} "
            f"ALTER COLUMN {enum_column_name} TYPE {type_name} "
            f"USING ({using}::text::{new_type_name});"
        )
    )

    if default is not None:
        op.execute(
            f"ALTER TABLE {table_name} "
            f"ALTER COLUMN {enum_column_name} SET DEFAULT '{default}';"
        )

    op.execute(f"DROP TYPE {type_name};")
    op.execute(f"ALTER TYPE {new_type_name} RENAME TO {type_name};")


def index_exists(name):
    alembic_connection = op.get_bind()
    result = alembic_connection.execute(
        f"SELECT exists(SELECT 1 FROM pg_indexes WHERE indexname = '{name}') as ix_exists;"
    ).first()
    return result.ix_exists
