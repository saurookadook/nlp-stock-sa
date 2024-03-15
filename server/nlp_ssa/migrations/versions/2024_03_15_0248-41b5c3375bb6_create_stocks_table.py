"""Create stocks table

Revision ID: 41b5c3375bb6
Revises: da61840d2497
Create Date: 2024-03-15 02:48:23.611529

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "41b5c3375bb6"
down_revision: Union[str, None] = "da61840d2497"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stocks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("quote_stock_symbol", sa.String(length=12), nullable=False),
        sa.Column("fall_stock_symbol", sa.String(length=255), nullable=False),
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
        sa.UniqueConstraint("fall_stock_symbol"),
        sa.UniqueConstraint("quote_stock_symbol"),
    )


def downgrade() -> None:
    op.drop_table("stocks")
