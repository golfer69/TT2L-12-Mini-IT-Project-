"""empty message

Revision ID: c7c40e1576ca
Revises: 
Create Date: 2024-06-07 13:39:43.329228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7c40e1576ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('votes', sa.Integer(), nullable=True))

    with op.batch_alter_table('community', schema=None) as batch_op:
        batch_op.drop_column('comm_profile_pic')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('community', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comm_profile_pic', sa.VARCHAR(length=10000), nullable=True))

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('votes')

    # ### end Alembic commands ###
