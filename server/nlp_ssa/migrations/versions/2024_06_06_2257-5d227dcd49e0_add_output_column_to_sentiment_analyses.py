"""Add output column to sentiment_analyses

Revision ID: 5d227dcd49e0
Revises: 28b6789d5b44
Create Date: 2024-06-06 22:57:25.578061

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union

import db

# revision identifiers, used by Alembic.
revision: str = "5d227dcd49e0"
down_revision: Union[str, None] = "28b6789d5b44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sentiment_analyses",
        sa.Column(
            "output",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("sentiment_analyses", "output")
