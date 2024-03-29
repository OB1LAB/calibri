"""empty message

Revision ID: ddc6ae1f627e
Revises: 
Create Date: 2022-10-26 19:27:45.954765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddc6ae1f627e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item_shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('type', sa.String(length=16), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('img_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('lvl', sa.Integer(), nullable=True),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('server',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('coffers', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('online', sa.Boolean(), nullable=True),
    sa.Column('vanish', sa.Boolean(), nullable=True),
    sa.Column('server_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('server_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=10), nullable=True),
    sa.Column('server_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_server_logs_date'), 'server_logs', ['date'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('discord_id', sa.String(length=20), nullable=True),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('currentWeekSalary', sa.Integer(), nullable=True),
    sa.Column('dt_role', sa.Integer(), nullable=True),
    sa.Column('tmrpg_role', sa.Integer(), nullable=True),
    sa.Column('birthday', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['dt_role'], ['role.id'], ),
    sa.ForeignKeyConstraint(['tmrpg_role'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=10), nullable=True),
    sa.Column('local_msg', sa.Integer(), nullable=True),
    sa.Column('global_msg', sa.Integer(), nullable=True),
    sa.Column('private_msg', sa.Integer(), nullable=True),
    sa.Column('warns', sa.Integer(), nullable=True),
    sa.Column('mutes', sa.Integer(), nullable=True),
    sa.Column('kicks', sa.Integer(), nullable=True),
    sa.Column('bans', sa.Integer(), nullable=True),
    sa.Column('online', sa.Integer(), nullable=True),
    sa.Column('online_vanish', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activity_date'), 'activity', ['date'], unique=False)
    op.create_table('app_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('log', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('history_buy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item_shop.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('history_vacation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_start', sa.DateTime(), nullable=True),
    sa.Column('date_end', sa.DateTime(), nullable=True),
    sa.Column('cause', sa.String(length=256), nullable=True),
    sa.Column('state', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('history_violation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('cause', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line', sa.String(length=256), nullable=True),
    sa.Column('server_logs_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['server_logs_id'], ['server_logs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('line')
    op.drop_table('history_violation')
    op.drop_table('history_vacation')
    op.drop_table('history_buy')
    op.drop_table('app_logs')
    op.drop_index(op.f('ix_activity_date'), table_name='activity')
    op.drop_table('activity')
    op.drop_table('user')
    op.drop_index(op.f('ix_server_logs_date'), table_name='server_logs')
    op.drop_table('server_logs')
    op.drop_table('player')
    op.drop_table('server')
    op.drop_table('role')
    op.drop_table('item_shop')
    # ### end Alembic commands ###
