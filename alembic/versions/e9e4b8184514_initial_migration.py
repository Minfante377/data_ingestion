"""Initial Migration

Revision ID: e9e4b8184514
Revises: 863583835f2d
Create Date: 2024-06-19 13:27:37.943151

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e9e4b8184514"
down_revision: Union[str, None] = "863583835f2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
