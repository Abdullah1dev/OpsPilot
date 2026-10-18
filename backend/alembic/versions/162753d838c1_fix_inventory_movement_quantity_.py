"""Fix inventory movement quantity constraint

Revision ID: 162753d838c1
Revises: f945878e8e71
Create Date: 2026-10-18 23:53:11.499463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '162753d838c1'
down_revision: Union[str, Sequence[str], None] = 'f945878e8e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.drop_constraint(
        "ck_inventory_movements_quantity_positive",
        "inventory_movements",
        type_="check",
    )

    op.create_check_constraint(
        "ck_inventory_movements_quantity_valid",
        "inventory_movements",
        """
        (movement_type = 'ADJUSTMENT' AND quantity >= 0)
        OR
        (movement_type IN ('RECEIPT', 'ISSUE') AND quantity > 0)
        """,
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_inventory_movements_quantity_valid",
        "inventory_movements",
        type_="check",
    )

    op.create_check_constraint(
        "ck_inventory_movements_quantity_positive",
        "inventory_movements",
        "quantity > 0",
    )
