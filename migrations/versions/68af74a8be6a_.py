"""empty message

Revision ID: 68af74a8be6a
Revises: df32db4fe48b
Create Date: 2023-11-06 00:37:48.753091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68af74a8be6a'
down_revision = 'df32db4fe48b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('got_coupon_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.drop_column('got_coupon_date')

    # ### end Alembic commands ###
