"""Correct type on quote_stock_symbol columns

Revision ID: 34ce88232a6f
Revises: 3e4697a5822d
Create Date: 2024-04-30 01:10:21.433950

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "34ce88232a6f"
down_revision: Union[str, None] = "3e4697a5822d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        None, "article_data", "stocks", ["quote_stock_symbol"], ["quote_stock_symbol"]
    )
    op.create_foreign_key(
        None,
        "sentiment_analyses",
        "stocks",
        ["quote_stock_symbol"],
        ["quote_stock_symbol"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "sentiment_analyses_quote_stock_symbol_fkey",
        "sentiment_analyses",
        type_="foreignkey",
    )
    op.drop_constraint(
        "article_data_quote_stock_symbol_fkey", "article_data", type_="foreignkey"
    )
