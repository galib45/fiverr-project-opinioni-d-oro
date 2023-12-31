"""empty message

Revision ID: 3713b76e9998
Revises: f8d3b6c5c756
Create Date: 2023-12-23 00:18:02.431126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3713b76e9998'
down_revision = 'f8d3b6c5c756'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.drop_column('settings')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.add_column(sa.Column('settings', sa.VARCHAR(), nullable=True))

    # ### end Alembic commands ###
