"""Add thumbnail_image_url column to article_data

Revision ID: b327af6cc15c
Revises: d83a8f4e77f5
Create Date: 2024-05-11 14:39:30.287695

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "b327af6cc15c"
down_revision: Union[str, None] = "d83a8f4e77f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "article_data", sa.Column("thumbnail_image_url", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("article_data", "thumbnail_image_url")
