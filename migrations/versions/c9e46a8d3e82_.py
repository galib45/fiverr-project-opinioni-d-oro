"""empty message

Revision ID: c9e46a8d3e82
Revises: 3713b76e9998
Create Date: 2023-12-23 00:18:34.629943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9e46a8d3e82'
down_revision = '3713b76e9998'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.add_column(sa.Column('general_coupon_offer', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.drop_column('general_coupon_offer')

    # ### end Alembic commands ###