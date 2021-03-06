"""added date to era model

Revision ID: 897af3ad5744
Revises: a90a17bb8fbf
Create Date: 2022-04-25 20:13:56.843340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '897af3ad5744'
down_revision = 'a90a17bb8fbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('era', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.String()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('era', schema=None) as batch_op:
        batch_op.drop_column('date')

    # ### end Alembic commands ###
