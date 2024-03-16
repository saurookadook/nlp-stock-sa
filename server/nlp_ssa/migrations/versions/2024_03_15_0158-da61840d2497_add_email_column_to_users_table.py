"""Add email column to users table

Revision ID: da61840d2497
Revises: b6fb17fa3666
Create Date: 2024-03-15 01:58:34.379749

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "da61840d2497"
down_revision: Union[str, None] = "b6fb17fa3666"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String(length=255), nullable=False))
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.drop_column("users", "email")
