"""Infourth migration

Revision ID: f2e21c628aae
Revises: c2e2abb878aa
Create Date: 2019-03-02 16:37:37.371009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2e21c628aae'
down_revision = 'c2e2abb878aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscribe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscribe_email'), 'subscribe', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscribe_email'), table_name='subscribe')
    op.drop_table('subscribe')
    # ### end Alembic commands ###
