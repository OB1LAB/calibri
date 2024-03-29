"""empty message

Revision ID: 4dc02c06009e
Revises: a1595c6ad386
Create Date: 2022-11-03 17:19:02.687951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dc02c06009e'
down_revision = 'a1595c6ad386'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history_buy', sa.Column('server_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'history_buy', 'server', ['server_id'], ['id'])
    op.add_column('history_vacation', sa.Column('server_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'history_vacation', 'server', ['server_id'], ['id'])
    op.drop_column('history_vacation', 'state')
    op.add_column('history_violation', sa.Column('server_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'history_violation', 'server', ['server_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'history_violation', type_='foreignkey')
    op.drop_column('history_violation', 'server_id')
    op.add_column('history_vacation', sa.Column('state', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'history_vacation', type_='foreignkey')
    op.drop_column('history_vacation', 'server_id')
    op.drop_constraint(None, 'history_buy', type_='foreignkey')
    op.drop_column('history_buy', 'server_id')
    # ### end Alembic commands ###
