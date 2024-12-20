"""add created_by to task table

Revision ID: ea3f6133500a
Revises: ad041e2e6796
Create Date: 2024-11-09 14:46:12.620701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea3f6133500a'
down_revision = 'ad041e2e6796'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('created_by', sa.Integer(), nullable=False))
    op.add_column('tasks', sa.Column('reviewed_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'users', ['created_by'], ['id'])
    op.create_foreign_key(None, 'tasks', 'users', ['reviewed_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'reviewed_by')
    op.drop_column('tasks', 'created_by')
    # ### end Alembic commands ###
