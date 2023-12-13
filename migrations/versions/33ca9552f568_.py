"""empty message

Revision ID: 33ca9552f568
Revises: e96da2c24076
Create Date: 2023-12-13 23:58:31.094087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33ca9552f568'
down_revision = 'e96da2c24076'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.add_column(sa.Column('package_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.drop_column('package_id')

    # ### end Alembic commands ###
