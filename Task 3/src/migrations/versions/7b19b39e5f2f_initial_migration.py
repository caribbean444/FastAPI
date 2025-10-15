"""initial migration

Revision ID: 7b19b39e5f2f
Revises: 
Create Date: 2025-10-15 00:06:30.090567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7b19b39e5f2f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('locations', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('hotels')
