"""empty message

Revision ID: a1595c6ad386
Revises: 285240643ca1
Create Date: 2022-11-02 23:12:19.943677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1595c6ad386'
down_revision = '285240643ca1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_shop', sa.Column('stack', sa.Integer(), nullable=True))
    op.drop_column('item_shop', 'img_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_shop', sa.Column('img_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column('item_shop', 'stack')
    # ### end Alembic commands ###