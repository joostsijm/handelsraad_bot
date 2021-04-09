"""add_money_to_transaction_detail

Revision ID: d7a42f1d8240
Revises: 3583779127ff
Create Date: 2021-04-09 10:20:38.905807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7a42f1d8240'
down_revision = '3583779127ff'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transaction_detail', sa.Column('money', sa.BigInteger(), nullable=False))


def downgrade():
    op.drop_column('transaction_detail', 'money')
