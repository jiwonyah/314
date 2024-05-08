"""empty message

Revision ID: e3c100b953c1
Revises: 704ec3f7ebea
Create Date: 2024-05-06 01:52:01.614584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3c100b953c1'
down_revision = '704ec3f7ebea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propertyListing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.create_foreign_key(batch_op.f('fk_propertyListing_user_id_user'), 'user', ['user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_userid'), ['userid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_userid'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')

    with op.batch_alter_table('propertyListing', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_propertyListing_user_id_user'), type_='foreignkey')
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
