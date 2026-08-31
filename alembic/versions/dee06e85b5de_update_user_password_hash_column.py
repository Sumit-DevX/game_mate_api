"""update user password_hash column

Revision ID: dee06e85b5de
Revises: f67062dc0b7c
Create Date: 2026-08-31 21:39:13.101204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dee06e85b5de'
down_revision: Union[str, Sequence[str], None] = 'f67062dc0b7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("gamemate_user", "password_hash", nullable=False)
    pass


def downgrade() -> None:
    op.alter_column("gamemate_user", "password_hash", nullable=True)
    pass
