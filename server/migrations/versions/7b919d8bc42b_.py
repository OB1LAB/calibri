"""empty message

Revision ID: 7b919d8bc42b
Revises: 8e72f319e316
Create Date: 2022-11-03 23:49:35.742581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b919d8bc42b'
down_revision = '8e72f319e316'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_shop', sa.Column('categories', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item_shop', 'categories')
    # ### end Alembic commands ###
