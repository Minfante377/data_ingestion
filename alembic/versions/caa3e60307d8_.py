"""empty message

Revision ID: caa3e60307d8
Revises: e9e4b8184514
Create Date: 2024-06-19 14:14:04.649522

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "caa3e60307d8"
down_revision: Union[str, None] = "e9e4b8184514"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
