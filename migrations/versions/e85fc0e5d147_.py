"""empty message

Revision ID: e85fc0e5d147
Revises: 959a9fb50ed3
Create Date: 2024-05-15 01:49:19.872412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e85fc0e5d147'
down_revision = '959a9fb50ed3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('profileName', sa.String(length=50), nullable=False),
    sa.Column('profileDescription', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('profileName', name=op.f('pk_profile')),
    sa.UniqueConstraint('profileName', name=op.f('uq_profile_profileName'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile')
    # ### end Alembic commands ###
