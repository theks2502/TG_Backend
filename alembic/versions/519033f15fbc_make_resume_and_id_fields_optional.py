"""make resume and id fields optional

Revision ID: 519033f15fbc
Revises: b90706cd180b
Create Date: 2025-12-26 17:56:24.891087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '519033f15fbc'
down_revision: Union[str, Sequence[str], None] = 'b90706cd180b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "hiring_application",
        "resume_file",
        existing_type=sa.String(),
        nullable=True
    )

    op.alter_column(
        "hiring_application",
        "id_proof_file",
        existing_type=sa.String(),
        nullable=True
    )

    op.alter_column(
        "hiring_application",
        "id_proof_type",
        existing_type=sa.String(),
        nullable=True
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "hiring_application",
        "resume_file",
        existing_type=sa.String(),
        nullable=False
    )

    op.alter_column(
        "hiring_application",
        "id_proof_file",
        existing_type=sa.String(),
        nullable=False
    )

    op.alter_column(
        "hiring_application",
        "id_proof_type",
        existing_type=sa.String(),
        nullable=False
    )
    pass
