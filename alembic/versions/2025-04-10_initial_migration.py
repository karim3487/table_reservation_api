"""Initial migration

Revision ID: 9bbacd88b2bc
Revises:
Create Date: 2025-04-10 17:04:16.528827

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9bbacd88b2bc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tables",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("seats", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_tables_id"), "tables", ["id"], unique=False)
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("customer_name", sa.String(), nullable=False),
        sa.Column("table_id", sa.Integer(), nullable=False),
        sa.Column("reservation_time", sa.DateTime(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["tables.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reservations_id"), "reservations", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_reservations_id"), table_name="reservations")
    op.drop_table("reservations")
    op.drop_index(op.f("ix_tables_id"), table_name="tables")
    op.drop_table("tables")
    # ### end Alembic commands ###
