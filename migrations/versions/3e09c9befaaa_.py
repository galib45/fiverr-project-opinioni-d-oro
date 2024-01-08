"""empty message

Revision ID: 3e09c9befaaa
Revises: f006eef49cf2
Create Date: 2024-01-08 10:15:54.725769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e09c9befaaa'
down_revision = 'f006eef49cf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coupon', schema=None) as batch_op:
        batch_op.drop_column('redeemed')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coupon', schema=None) as batch_op:
        batch_op.add_column(sa.Column('redeemed', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
