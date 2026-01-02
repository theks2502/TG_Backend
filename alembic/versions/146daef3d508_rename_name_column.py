"""rename name column

Revision ID: 146daef3d508
Revises: 1449aaa46a16
Create Date: 2025-12-18 06:52:08.625913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '146daef3d508'
down_revision: Union[str, Sequence[str], None] = '1449aaa46a16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "hiring_application",
        "full_name",
        new_column_name="name"
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "hiring_application",
        "name",
        new_column_name="full_name"
    )

    pass
