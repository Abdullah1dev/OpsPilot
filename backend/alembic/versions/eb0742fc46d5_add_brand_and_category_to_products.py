"""add brand and category to products

Revision ID: eb0742fc46d5
Revises: 162753d838c1
Create Date: 2026-10-19 21:28:25.129361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb0742fc46d5'
down_revision: Union[str, Sequence[str], None] = '162753d838c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None





def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("brand", sa.String(length=100), nullable=False),
    )
    op.add_column(
        "products",
        sa.Column("category", sa.String(length=100), nullable=False),
    )
    op.create_index(
        op.f("ix_products_brand"),
        "products",
        ["brand"],
        unique=False,
    )
    op.create_index(
        op.f("ix_products_category"),
        "products",
        ["category"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_products_category"), table_name="products")
    op.drop_index(op.f("ix_products_brand"), table_name="products")
    op.drop_column("products", "category")
    op.drop_column("products", "brand")
