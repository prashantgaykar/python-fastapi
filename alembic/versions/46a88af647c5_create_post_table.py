"""create post table

Revision ID: 46a88af647c5
Revises: 0a94855c1c53
Create Date: 2022-01-12 20:34:16.153812

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import false


# revision identifiers, used by Alembic.
revision = '46a88af647c5'
down_revision = '0a94855c1c53'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), primary_key=True,
                              nullable=false, autoincrement=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
