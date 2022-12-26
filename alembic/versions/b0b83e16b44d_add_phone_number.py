"""add phone number

Revision ID: b0b83e16b44d
Revises: 231792aec736
Create Date: 2022-12-22 21:44:40.005371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0b83e16b44d'
down_revision = '231792aec736'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.VARCHAR(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
