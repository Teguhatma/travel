"""country

Revision ID: cbcf36ca7352
Revises: 92d053b0a0fb
Create Date: 2019-03-18 21:26:43.988042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbcf36ca7352'
down_revision = '92d053b0a0fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    op.add_column('kontak', sa.Column('country', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'kontak', 'country', ['country'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'kontak', type_='foreignkey')
    op.drop_column('kontak', 'country')
    op.drop_table('country')
    # ### end Alembic commands ###
