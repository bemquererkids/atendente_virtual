"""Merge das múltiplas heads

Revision ID: a8faeaae60cc
Revises: 3821d8101e7c, renomear_id_para_id_contexto
Create Date: 2025-05-04 12:49:30.361589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8faeaae60cc'
down_revision: Union[str, None] = ('3821d8101e7c', 'renomear_id_para_id_contexto')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
