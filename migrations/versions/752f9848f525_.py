"""empty message

Revision ID: 752f9848f525
Revises: 2e70e7b640ff
Create Date: 2024-12-05 21:03:39.696145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '752f9848f525'
down_revision = '2e70e7b640ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.alter_column('spent',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.alter_column('money',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.alter_column('money',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.alter_column('spent',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###
