"""add mode of transport column to manali table

Revision ID: 39828302fe9f
Revises: 73709cb3a313
Create Date: 2025-11-23 12:20:37.867141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39828302fe9f'
down_revision: Union[str, Sequence[str], None] = '73709cb3a313'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('manali' , sa.Column('mode_of_transport' , sa.String() , nullable=False , server_default='Bus'))
    pass


def downgrade() :
    op.drop_column('manali' , 'mode_of_transport')
    pass
