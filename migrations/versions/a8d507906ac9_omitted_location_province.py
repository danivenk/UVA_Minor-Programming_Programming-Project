"""omitted location_province

Revision ID: a8d507906ac9
Revises: 0421ebd86d68
Create Date: 2020-04-16 17:46:21.706472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8d507906ac9'
down_revision = '0421ebd86d68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stops', 'location_province')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stops', sa.Column('location_province', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###