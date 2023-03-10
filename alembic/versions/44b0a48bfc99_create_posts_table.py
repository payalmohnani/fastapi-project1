"""Create Posts table

Revision ID: 44b0a48bfc99
Revises: 
Create Date: 2023-03-08 02:10:43.290418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44b0a48bfc99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    )
    


def downgrade() -> None:
    op.drop_table('posts')
