"""added company class

Revision ID: a721a707754b
Revises: 12e094c7d1ed
Create Date: 2020-05-10 22:26:41.328036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a721a707754b'
down_revision = '12e094c7d1ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('short_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('lines', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'lines', 'companies', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'lines', type_='foreignkey')
    op.drop_column('lines', 'company_id')
    op.drop_table('companies')
    # ### end Alembic commands ###
