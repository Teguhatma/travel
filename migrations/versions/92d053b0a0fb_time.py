"""time

Revision ID: 92d053b0a0fb
Revises: 688c9b101c89
Create Date: 2019-03-18 21:14:23.265581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92d053b0a0fb'
down_revision = '688c9b101c89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Products', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_Products_timestamp'), 'Products', ['timestamp'], unique=False)
    op.add_column('kontak', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_kontak_timestamp'), 'kontak', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_kontak_timestamp'), table_name='kontak')
    op.drop_column('kontak', 'timestamp')
    op.drop_index(op.f('ix_Products_timestamp'), table_name='Products')
    op.drop_column('Products', 'timestamp')
    # ### end Alembic commands ###
