"""Create sources and source_association tables

Revision ID: fb5b0f6e453d
Revises: 5d227dcd49e0
Create Date: 2024-06-08 00:29:00.879655

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

import db
from constants import SourceDiscriminatorEnum
from migrations.alembic_utilities import create_pg_enum, drop_pg_enum

# revision identifiers, used by Alembic.
revision: str = "fb5b0f6e453d"
down_revision: Union[str, None] = "5d227dcd49e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    source_discriminators = create_pg_enum(
        SourceDiscriminatorEnum.db_type_name(),
        [x.value for x in SourceDiscriminatorEnum],
    )

    op.create_table(
        "source_association",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "discriminator",
            source_discriminators,
            nullable=False,
            server_default=SourceDiscriminatorEnum.get_default_value(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sources",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("association_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["association_id"],
            ["source_association.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "article_data", sa.Column("source_association_id", sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        None, "article_data", "source_association", ["source_association_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "article_data_source_association_id_fkey", "article_data", type_="foreignkey"
    )
    op.drop_column("article_data", "source_association_id")
    op.drop_table("sources")
    op.drop_table("source_association")
    drop_pg_enum(
        SourceDiscriminatorEnum.db_type_name(),
        [x.value for x in SourceDiscriminatorEnum],
    )
