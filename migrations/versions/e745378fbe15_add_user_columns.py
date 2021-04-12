"""add_user_columns

Revision ID: e745378fbe15
Revises: 70e0349b9c91
Create Date: 2021-04-12 10:44:51.162723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e745378fbe15'
down_revision = '70e0349b9c91'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('rival_region_id', sa.BigInteger(), nullable=True))
    op.add_column('user', sa.Column('telegram_username', sa.String(), nullable=False))


def downgrade():
    op.drop_column('user', 'telegram_username')
    op.drop_column('user', 'rival_region_id')
