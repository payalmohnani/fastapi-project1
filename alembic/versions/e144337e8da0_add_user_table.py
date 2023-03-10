"""Add user table

Revision ID: e144337e8da0
Revises: af9ba7f71c25
Create Date: 2023-03-08 02:33:31.656879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e144337e8da0'
down_revision = 'af9ba7f71c25'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(),nullable=False,primary_key=True ),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('users')
