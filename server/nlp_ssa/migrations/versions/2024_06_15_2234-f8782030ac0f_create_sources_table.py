"""Create sources table

Revision ID: f8782030ac0f
Revises: 5d227dcd49e0
Create Date: 2024-06-15 22:34:08.780730

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db
from constants import SourceDiscriminatorEnum
from migrations.alembic_utilities import create_pg_enum, drop_pg_enum

# revision identifiers, used by Alembic.
revision: str = "f8782030ac0f"
down_revision: Union[str, None] = "5d227dcd49e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


pg_enum_args = [
    SourceDiscriminatorEnum.db_type_name(),
    [x.value for x in SourceDiscriminatorEnum],
]


def upgrade() -> None:
    source_discriminators = create_pg_enum(*pg_enum_args)

    op.create_table(
        "sources",
        sa.Column(
            "data_type",
            source_discriminators,
            nullable=False,
        ),
        sa.Column("data_type_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            db.db.ArrowDateClass(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            db.db.ArrowDateClass(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("data_type_id"),
    )


def downgrade() -> None:
    op.drop_table("sources")
    drop_pg_enum(*pg_enum_args)
