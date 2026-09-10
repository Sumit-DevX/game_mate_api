"""add unique constraint to email column in user's table

Revision ID: fbc4cc508b4c
Revises: dee06e85b5de
Create Date: 2026-09-10 21:38:05.054911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbc4cc508b4c'
down_revision: Union[str, Sequence[str], None] = 'dee06e85b5de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("gamemate_user","email",unique=True)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("gamemate_user","email",unique=False)
    pass
