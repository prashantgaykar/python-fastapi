"""add table users

Revision ID: c3cf197ffd42
Revises: c0c0eec53574
Create Date: 2022-01-12 21:09:09.462394

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.functions import now


# revision identifiers, used by Alembic.
revision = 'c3cf197ffd42'
down_revision = 'c0c0eec53574'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), index=True,
                              primary_key=True, nullable=False,),
                    sa.Column('email', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=now()))
    pass


def downgrade():
    op.drop_table('users')
    pass
