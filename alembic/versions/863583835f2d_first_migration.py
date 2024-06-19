"""first migration

Revision ID: 863583835f2d
Revises: 2ad8e3c04858
Create Date: 2024-06-19 13:24:41.370065

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "863583835f2d"
down_revision: Union[str, None] = "2ad8e3c04858"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
