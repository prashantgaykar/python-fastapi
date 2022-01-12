"""add other columns to posts

Revision ID: c0c0eec53574
Revises: 9418eb720411
Create Date: 2022-01-12 20:57:16.583227

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.functions import now


# revision identifiers, used by Alembic.
revision = 'c0c0eec53574'
down_revision = '9418eb720411'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=now()))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
