"""Insecond migration

Revision ID: 16bd6edd51e0
Revises: 2f680ab8224a
Create Date: 2019-03-02 10:33:28.993366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16bd6edd51e0'
down_revision = '2f680ab8224a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comments_user_id_fkey', 'comments', type_='foreignkey')
    op.drop_column('comments', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('comments_user_id_fkey', 'comments', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
