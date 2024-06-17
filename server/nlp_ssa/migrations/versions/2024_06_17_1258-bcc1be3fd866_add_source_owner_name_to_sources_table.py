"""Add source_owner_name to sources table

Revision ID: bcc1be3fd866
Revises: 4eedb26df2fd
Create Date: 2024-06-17 12:58:35.118213

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "bcc1be3fd866"
down_revision: Union[str, None] = "4eedb26df2fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("sources", sa.Column("source_owner_name", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("sources", "source_owner_name")
