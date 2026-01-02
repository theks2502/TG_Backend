"""rename phone and email columns

Revision ID: 1449aaa46a16
Revises: 2c81ea837985
Create Date: 2025-12-18 06:48:11.203612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1449aaa46a16'
down_revision: Union[str, Sequence[str], None] = '2c81ea837985'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "hiring_application",
        "phone_number",
        new_column_name="phone_number"
    )

    op.alter_column(
        "hiring_application",
        "email_address",
        new_column_name="email_address"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "hiring_application",
        "contact_number",
        new_column_name="phone"
    )

    op.alter_column(
        "hiring_application",
        "email_address",
        new_column_name="email"
    )
    
