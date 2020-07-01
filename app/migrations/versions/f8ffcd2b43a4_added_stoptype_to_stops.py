"""added stoptype to stops

Revision ID: f8ffcd2b43a4
Revises: 969c7d0201e6
Create Date: 2020-04-29 16:22:25.089338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8ffcd2b43a4'
down_revision = '969c7d0201e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stops', sa.Column('stoptype', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stops', 'stoptype')
    # ### end Alembic commands ###