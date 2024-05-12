"""Create analysis_views table

Revision ID: f6c3fbfda286
Revises: 41b5c3375bb6
Create Date: 2024-03-16 04:34:23.618392

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "f6c3fbfda286"
down_revision: Union[str, None] = "41b5c3375bb6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analysis_views",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("source_group_id", sa.UUID(), nullable=False),
        # sa.Column("owner_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
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
    op.drop_table("analysis_views")
