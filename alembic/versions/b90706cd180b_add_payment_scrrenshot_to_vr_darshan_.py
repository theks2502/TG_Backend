"""add payment scrrenshot to VR Darshan table

Revision ID: b90706cd180b
Revises: 146daef3d508
Create Date: 2025-12-20 19:06:11.450732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b90706cd180b'
down_revision: Union[str, Sequence[str], None] = '146daef3d508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "vr_darshan_booking",
        sa.Column("payment_screenshot", sa.String(length=255), nullable=True)
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("vr_darshan_booking", "payment_screenshot")
    
