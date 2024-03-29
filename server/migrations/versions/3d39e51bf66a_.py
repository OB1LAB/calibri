"""empty message

Revision ID: 3d39e51bf66a
Revises: d4582a256b57
Create Date: 2022-10-29 18:20:35.789632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d39e51bf66a'
down_revision = 'd4582a256b57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_discord_id_key', 'user', type_='unique')
    op.create_index(op.f('ix_user_discord_id'), 'user', ['discord_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_discord_id'), table_name='user')
    op.create_unique_constraint('user_discord_id_key', 'user', ['discord_id'])
    # ### end Alembic commands ###
