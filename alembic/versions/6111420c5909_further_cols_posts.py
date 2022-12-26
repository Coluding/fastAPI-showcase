"""further cols posts

Revision ID: 6111420c5909
Revises: 946bc1a62dd2
Create Date: 2022-12-22 21:34:01.464263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6111420c5909'
down_revision = '946bc1a62dd2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass