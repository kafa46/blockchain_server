"""empty message

Revision ID: 7319ade43579
Revises: 
Create Date: 2023-06-28 15:28:13.545617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7319ade43579'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('block',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prev_hash', sa.String(length=300), nullable=True),
    sa.Column('nonce', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mining_node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_addr', sa.String(length=50), nullable=True),
    sa.Column('port', sa.String(length=10), nullable=True),
    sa.Column('domain_name', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('last_access', sa.DateTime(), nullable=True),
    sa.Column('initial_access', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.Integer(), nullable=True),
    sa.Column('send_addr', sa.String(length=300), nullable=True),
    sa.Column('recv_addr', sa.String(length=300), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['block.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('mining_node')
    op.drop_table('block')
    # ### end Alembic commands ###
