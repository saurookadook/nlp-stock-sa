"""Add foreign key relationships between sentiment_analyses and sources

Revision ID: 4eedb26df2fd
Revises: f8782030ac0f
Create Date: 2024-06-16 14:49:11.585906

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "4eedb26df2fd"
down_revision: Union[str, None] = "f8782030ac0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


sa_source_id_fk_constraint_name = "sentiment_analyses_source_id_fkey"


def upgrade() -> None:
    op.add_column(
        "sentiment_analyses", sa.Column("source_id", sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        sa_source_id_fk_constraint_name,
        "sentiment_analyses",
        "sources",
        ["source_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        sa_source_id_fk_constraint_name, "sentiment_analyses", type_="foreignkey"
    )
    op.drop_column("sentiment_analyses", "source_id")
