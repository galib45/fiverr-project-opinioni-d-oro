"""empty message

Revision ID: df32db4fe48b
Revises: 0e0fb498a814
Create Date: 2023-11-05 22:55:11.758695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df32db4fe48b'
down_revision = '0e0fb498a814'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###
