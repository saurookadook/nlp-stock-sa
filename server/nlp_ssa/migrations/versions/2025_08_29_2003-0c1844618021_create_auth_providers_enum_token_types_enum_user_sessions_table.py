"""Create auth_providers enum, token_types enum, and user_sessions table

Revision ID: 0c1844618021
Revises: bcc1be3fd866
Create Date: 2025-08-29 20:03:53.857906

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union

import db
from constants import AuthProviderEnum, TokenTypeEnum
from migrations.alembic_utilities import create_pg_enum, drop_pg_enum

# revision identifiers, used by Alembic.
revision: str = "0c1844618021"
down_revision: Union[str, None] = "bcc1be3fd866"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

auth_providers_pg_enum_args = [
    AuthProviderEnum.db_type_name(),
    [x.value for x in AuthProviderEnum],
]

token_types_pg_enum_args = [
    TokenTypeEnum.db_type_name(),
    [x.value for x in TokenTypeEnum],
]


def upgrade() -> None:
    auth_providers = create_pg_enum(*auth_providers_pg_enum_args)
    token_types = create_pg_enum(*token_types_pg_enum_args)

    op.create_table(
        "user_sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("access_token", sa.String(), nullable=False, unique=True),
        sa.Column("auth_provider", auth_providers, nullable=False),
        sa.Column("expires_in", sa.INTEGER(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=True),
        sa.Column(
            "refresh_token_expires_in",
            sa.INTEGER(),
            nullable=True,
        ),
        sa.Column(
            "token_type",
            token_types,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            db.db.ArrowDateClass(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            db.db.ArrowDateClass(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("refresh_token"),
    )


def downgrade() -> None:
    op.drop_table("user_sessions")
    drop_pg_enum(*token_types_pg_enum_args)
    drop_pg_enum(*auth_providers_pg_enum_args)
