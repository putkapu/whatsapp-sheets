"""create users table

Revision ID: 62c82bc49e16
Revises: 
Create Date: 2025-05-05 10:53:53.905429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62c82bc49e16'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('phone_number', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('google_sheets_url', sa.String(length=500), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
