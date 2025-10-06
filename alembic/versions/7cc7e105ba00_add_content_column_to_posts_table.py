"""add content column to posts table

Revision ID: 7cc7e105ba00
Revises: 99e757079014
Create Date: 2024-12-22 19:55:13.470776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cc7e105ba00'
down_revision: Union[str, None] = '99e757079014'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
