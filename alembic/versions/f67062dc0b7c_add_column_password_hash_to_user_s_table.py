"""Add column password_hash to user's table

Revision ID: f67062dc0b7c
Revises: 
Create Date: 2026-08-28 16:26:20.005764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f67062dc0b7c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('gamemate_user', sa.Column('password_hash', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('gamemate_user', 'password_hash')
    pass
