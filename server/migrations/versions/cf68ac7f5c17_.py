"""empty message

Revision ID: cf68ac7f5c17
Revises: e71f76be6b52
Create Date: 2022-11-01 00:21:29.417306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf68ac7f5c17'
down_revision = 'e71f76be6b52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player')
    op.drop_index('ix_server_logs_date', table_name='server_logs')
    op.drop_table('server_logs')
    op.drop_index('ix_activity_date', table_name='activity')
    op.drop_table('activity')
    op.drop_table('line')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('line',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('line', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('serverLogs_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['serverLogs_id'], ['server_logs.id'], name='line_serverLogs_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='line_pkey')
    )
    op.create_table('activity',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('local_msg', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('global_msg', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('private_msg', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('warns', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('mutes', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('kicks', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bans', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('online', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('online_vanish', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('player_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], name='activity_player_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='activity_pkey')
    )
    op.create_index('ix_activity_date', 'activity', ['date'], unique=False)
    op.create_table('server_logs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('server_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], name='server_logs_server_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='server_logs_pkey')
    )
    op.create_index('ix_server_logs_date', 'server_logs', ['date'], unique=False)
    op.create_table('player',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=16), autoincrement=False, nullable=True),
    sa.Column('online', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('vanish', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('server_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], name='player_server_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='player_pkey')
    )
    # ### end Alembic commands ###
