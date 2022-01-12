"""add foreign key to table users

Revision ID: 76036cfb45f1
Revises: c3cf197ffd42
Create Date: 2022-01-12 21:14:55.124526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76036cfb45f1'
down_revision = 'c3cf197ffd42'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(constraint_name='post_user_fkey', source_table='posts',
                          referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint(constraint_name='post_user_fkey', table_name='posts')
    op.drop_column(table_name='posts', column_name='user_id')
    pass
