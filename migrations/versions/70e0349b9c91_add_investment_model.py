"""add_investment_model

Revision ID: 70e0349b9c91
Revises: d7a42f1d8240
Create Date: 2021-04-12 10:22:14.176940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70e0349b9c91'
down_revision = 'd7a42f1d8240'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('investment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('user', 'investment')


def downgrade():
    op.add_column('user', sa.Column('investment', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_table('investment')
