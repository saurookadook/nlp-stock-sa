"""Create one-owner-to-many-analysis-views relationship

Revision ID: a6c48b96b09c
Revises: f6c3fbfda286
Create Date: 2024-03-17 20:24:42.602688

"""

from alembic import op
from typing import Sequence, Union

import db


# revision identifiers, used by Alembic.
revision: str = "a6c48b96b09c"
down_revision: Union[str, None] = "f6c3fbfda286"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(None, "analysis_views", "users", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "analysis_views", type_="foreignkey")
