"""added stopnumber to stops

Revision ID: beef422a19bc
Revises: ab3a72b0d44e
Create Date: 2020-05-13 17:26:19.221084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beef422a19bc'
down_revision = 'ab3a72b0d44e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stops', sa.Column('stopnumber', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stops', 'stopnumber')
    # ### end Alembic commands ###
