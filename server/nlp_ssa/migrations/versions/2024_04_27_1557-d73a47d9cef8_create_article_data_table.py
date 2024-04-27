"""Create article_data table

Revision ID: d73a47d9cef8
Revises: a6c48b96b09c
Create Date: 2024-04-27 15:57:11.644797

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "d73a47d9cef8"
down_revision: Union[str, None] = "a6c48b96b09c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "article_data",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("source_group_id", sa.UUID(), nullable=False),
        sa.Column("quote_stock_symbol", sa.String(length=10), nullable=False),
        sa.Column("source_url", sa.String(length=2048), nullable=False),
        sa.Column("sentence_tokens", sa.String(), nullable=True),
        sa.Column("raw_content", sa.String(), nullable=True),
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
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("article_data")
