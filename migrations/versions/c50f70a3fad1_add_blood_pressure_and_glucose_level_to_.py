"""Add blood_pressure and glucose_level to HealthData

Revision ID: c50f70a3fad1
Revises: 77fe75558dd3
Create Date: 2025-06-24 09:22:33.604867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c50f70a3fad1'
down_revision = '77fe75558dd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blood_pressure', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('glucose_level', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health_data', schema=None) as batch_op:
        batch_op.drop_column('glucose_level')
        batch_op.drop_column('blood_pressure')

    # ### end Alembic commands ###
