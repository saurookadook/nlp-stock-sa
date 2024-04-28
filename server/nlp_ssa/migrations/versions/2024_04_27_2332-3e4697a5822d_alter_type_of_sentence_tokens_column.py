"""Alter type of sentence_tokens column

Revision ID: 3e4697a5822d
Revises: d73a47d9cef8
Create Date: 2024-04-27 23:32:07.841773

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "3e4697a5822d"
down_revision: Union[str, None] = "d73a47d9cef8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


sentence_tokens_col_name = "sentence_tokens"


def upgrade() -> None:
    op.alter_column(
        "article_data",
        sentence_tokens_col_name,
        type_=postgresql.ARRAY(sa.String),
        postgresql_using=f"{sentence_tokens_col_name}::character varying[]",
    )


def downgrade() -> None:
    op.alter_column("article_data", sentence_tokens_col_name, type_=sa.String())
