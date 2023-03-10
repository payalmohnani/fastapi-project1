"""Adding last few columns to posts table.

Revision ID: a3bf48537b90
Revises: c53880d48413
Create Date: 2023-03-09 23:48:00.381559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3bf48537b90'
down_revision = 'c53880d48413'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
