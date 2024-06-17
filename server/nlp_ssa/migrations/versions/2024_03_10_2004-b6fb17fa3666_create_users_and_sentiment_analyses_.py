"""Create users and sentiment_analyses tables

Revision ID: b6fb17fa3666
Revises:
Create Date: 2024-03-10 20:04:52.620130

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

from constants import SentimentEnum
import db
from migrations.alembic_utilities import create_pg_enum, drop_pg_enum

# revision identifiers, used by Alembic.
revision: str = "b6fb17fa3666"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


pg_enum_args = [SentimentEnum.db_type_name(), [x.value for x in SentimentEnum]]


def upgrade() -> None:
    sentiments = create_pg_enum(*pg_enum_args)

    op.create_table(
        "sentiment_analyses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("quote_stock_symbol", sa.String(length=10), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column(
            "sentiment",
            sentiments,
            nullable=False,
            server_default=SentimentEnum.NEUTRAL.value,
        ),
        sa.Column("source_group_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            db.db.ArrowDateClass(timezone=True),
            # TODO: this should probably use sa.func.now()
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            db.db.ArrowDateClass(timezone=True),
            # TODO: this should probably use sa.func.now()
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("last_name", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            db.db.ArrowDateClass(timezone=True),
            # TODO: this should probably use sa.func.now()
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            db.db.ArrowDateClass(timezone=True),
            # TODO: this should probably use sa.func.now()
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("sentiment_analyses")
    drop_pg_enum(*pg_enum_args)
