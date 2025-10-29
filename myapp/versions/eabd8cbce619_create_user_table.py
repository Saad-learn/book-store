"""create User table

Revision ID: eabd8cbce619
Revises: 
Create Date: 2025-10-29 16:48:44.124603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eabd8cbce619'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.create_table(
    #     "employee",
    #     sa.column("id", sa.Integer, primary_key = True),
    #     sa.column("name", sa.String(50), nullable = False),
    #     sa.column("current", sa.Boolean, default = True)
    # )
    """Upgrade schema."""
    pass

def downgrade() -> None:
    # op.drop_table("employee")
    """Downgrade schema."""
    pass
