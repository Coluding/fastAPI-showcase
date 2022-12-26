"""user table

Revision ID: 946bc1a62dd2
Revises: 5df8a94bc65b
Create Date: 2022-12-22 21:32:20.047516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '946bc1a62dd2'
down_revision = '5df8a94bc65b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

def downgrade() -> None:
    op.drop_table('users')
