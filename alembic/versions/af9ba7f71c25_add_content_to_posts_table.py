"""Add content to posts table

Revision ID: af9ba7f71c25
Revises: 44b0a48bfc99
Create Date: 2023-03-08 02:26:08.470157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af9ba7f71c25'
down_revision = '44b0a48bfc99'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
