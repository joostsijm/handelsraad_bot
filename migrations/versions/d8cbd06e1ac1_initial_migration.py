"""initial_migration

Revision ID: d8cbd06e1ac1
Revises: 
Create Date: 2021-04-08 21:06:31.551560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8cbd06e1ac1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('limit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.SmallInteger(), nullable=False),
    sa.Column('amount', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('creator', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.SmallInteger(), nullable=False),
    sa.Column('amount', sa.BigInteger(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('transaction_detail')
    op.drop_table('transaction')
    op.drop_table('limit')
