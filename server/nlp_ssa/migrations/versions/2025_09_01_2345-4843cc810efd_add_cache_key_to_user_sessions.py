"""Add cache_key to user_sessions

Revision ID: 4843cc810efd
Revises: 0c1844618021
Create Date: 2025-09-01 23:45:23.185947

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "4843cc810efd"
down_revision: Union[str, None] = "0c1844618021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user_sessions", sa.Column("cache_key", sa.String(), nullable=True))
    op.create_unique_constraint(None, "user_sessions", ["cache_key"])


def downgrade() -> None:
    op.drop_constraint(None, "user_sessions", type_="unique")
    op.drop_column("user_sessions", "cache_key")
