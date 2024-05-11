"""Add and update article_data columns

Revision ID: d83a8f4e77f5
Revises: 34ce88232a6f
Create Date: 2024-05-09 13:37:18.871205

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "d83a8f4e77f5"
down_revision: Union[str, None] = "34ce88232a6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


sentence_tokens_col_name = "sentence_tokens"


def upgrade() -> None:
    op.add_column("article_data", sa.Column("author", sa.String(), nullable=True))
    op.add_column(
        "article_data",
        sa.Column(
            "last_updated_date", db.db.ArrowDateClass(timezone=True), nullable=True
        ),
    )
    op.add_column(
        "article_data",
        sa.Column("published_date", db.db.ArrowDateClass(timezone=True), nullable=True),
    )
    op.add_column("article_data", sa.Column("title", sa.String(), nullable=True))
    op.alter_column(
        "article_data",
        sentence_tokens_col_name,
        type_=sa.String(),
        postgresql_using=f"{sentence_tokens_col_name}::character varying",
    )


def downgrade() -> None:
    op.drop_column("article_data", "title")
    op.drop_column("article_data", "published_date")
    op.drop_column("article_data", "last_updated_date")
    op.drop_column("article_data", "author")
    op.alter_column(
        "article_data", sentence_tokens_col_name, type_=postgresql.ARRAY(sa.String)
    )
