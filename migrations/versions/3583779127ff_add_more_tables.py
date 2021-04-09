"""add_more_tables

Revision ID: 3583779127ff
Revises: d8cbd06e1ac1
Create Date: 2021-04-09 09:38:59.836940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3583779127ff'
down_revision = 'd8cbd06e1ac1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('chairman', sa.Boolean(), nullable=False),
    sa.Column('trader', sa.Boolean(), nullable=False),
    sa.Column('investor', sa.Boolean(), nullable=False),
    sa.Column('investment', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profit_type', sa.SmallInteger(), nullable=False),
    sa.Column('amount', sa.BigInteger(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('transaction', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'transaction', 'user', ['user_id'], ['id'])
    op.drop_column('transaction', 'creator')


def downgrade():
    op.add_column('transaction', sa.Column('creator', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_column('transaction', 'user_id')
    op.drop_table('profit')
    op.drop_table('user')
