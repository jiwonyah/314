"""empty message

Revision ID: 47a58bb286c7
Revises: b56f0980fec7
Create Date: 2024-05-06 22:10:33.549909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47a58bb286c7'
down_revision = 'b56f0980fec7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propertyListing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('view_counts', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propertyListing', schema=None) as batch_op:
        batch_op.drop_column('view_counts')

    # ### end Alembic commands ###