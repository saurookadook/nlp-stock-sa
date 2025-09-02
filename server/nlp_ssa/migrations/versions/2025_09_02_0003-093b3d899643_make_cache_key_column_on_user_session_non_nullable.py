"""Make cache_key column on user_session non-nullable

Revision ID: 093b3d899643
Revises: 4843cc810efd
Create Date: 2025-09-02 00:03:57.344081

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "093b3d899643"
down_revision: Union[str, None] = "4843cc810efd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "user_sessions",  # force formatting
        "cache_key",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "user_sessions",  # force formatting
        "cache_key",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
