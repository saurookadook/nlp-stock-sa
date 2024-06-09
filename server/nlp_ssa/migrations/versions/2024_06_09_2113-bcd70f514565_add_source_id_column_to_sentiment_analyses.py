"""Add source_id column to sentiment_analyses

Revision ID: bcd70f514565
Revises: fb5b0f6e453d
Create Date: 2024-06-09 21:13:55.035033

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "bcd70f514565"
down_revision: Union[str, None] = "fb5b0f6e453d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sentiment_analyses", sa.Column("source_id", sa.UUID(), nullable=True)
    )
    op.create_foreign_key(None, "sentiment_analyses", "sources", ["source_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(
        "sentiment_analyses_source_id_fkey", "sentiment_analyses", type_="foreignkey"
    )
    op.drop_column("sentiment_analyses", "source_id")
