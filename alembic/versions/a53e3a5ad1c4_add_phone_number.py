"""add phone number

Revision ID: a53e3a5ad1c4
Revises: 6b2bf3135cee
Create Date: 2024-12-22 20:44:12.594989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a53e3a5ad1c4'
down_revision: Union[str, None] = '6b2bf3135cee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    pass


def downgrade():
    op.drop_column('users', 'phone_number')
    pass
