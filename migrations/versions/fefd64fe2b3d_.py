"""empty message

Revision ID: fefd64fe2b3d
Revises: 9b975d5f0742
Create Date: 2019-04-26 15:30:52.569448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fefd64fe2b3d'
down_revision = '9b975d5f0742'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('conferences', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_conferences_enddate'), ['enddate'])
        batch_op.create_unique_constraint(batch_op.f('uq_conferences_startdate'), ['startdate'])
        batch_op.drop_column('start_date')
        batch_op.drop_column('end_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('conferences', schema=None) as batch_op:
        batch_op.add_column(sa.Column('end_date', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('start_date', sa.DATETIME(), nullable=True))
        batch_op.drop_constraint(batch_op.f('uq_conferences_startdate'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_conferences_enddate'), type_='unique')

    # ### end Alembic commands ###
