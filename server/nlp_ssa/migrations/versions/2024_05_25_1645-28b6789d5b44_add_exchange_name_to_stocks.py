"""Add exchange_name to stocks

Revision ID: 28b6789d5b44
Revises: b327af6cc15c
Create Date: 2024-05-25 16:45:17.088173

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "28b6789d5b44"
down_revision: Union[str, None] = "b327af6cc15c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "stocks", sa.Column("exchange_name", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("stocks", "exchange_name")
