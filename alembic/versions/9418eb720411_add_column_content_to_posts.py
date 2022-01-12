"""add column content to posts

Revision ID: 9418eb720411
Revises: 46a88af647c5
Create Date: 2022-01-12 20:48:04.170936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9418eb720411'
down_revision = '46a88af647c5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
