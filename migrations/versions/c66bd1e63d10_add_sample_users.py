"""add_sample_users

Revision ID: c66bd1e63d10
Revises: 62c82bc49e16
Create Date: 2025-05-05 11:30:49.795735

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c66bd1e63d10'
down_revision: Union[str, None] = '62c82bc49e16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO users (id, name, phone_number, password, created_at, updated_at, is_active, google_sheets_id, google_token) VALUES
        (1, 'Sample User', '+550000000000', 'password', '2025-05-05 10:53:53', '2025-05-05 10:53:53', TRUE, 'sample_google_sheets_id', 'sample_google_token');
    """) # type: ignore

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM users WHERE id = 1;
    """) # type: ignore
