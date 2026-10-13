
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.inventory.models import Inventory
from app.features.inventory.schemas import InventoryResponse
from app.features.products.models import Product


def get_inventory_by_product_name(
    db: Session,
    product_name: str,
) -> InventoryResponse | None:
    statement = (
        select(Product, Inventory)
        .join(Inventory, Inventory.product_id == Product.id)
        .where(Product.name.ilike(product_name.strip()))
    )

    result = db.execute(statement).first()

    if result is None:
        return None

    product, inventory = result

    return InventoryResponse(
        product_id=product.id,
        product_name=product.name,
        sku=product.sku,
        quantity_on_hand=inventory.quantity_on_hand,
        quantity_reserved=inventory.quantity_reserved,
        quantity_available=(
            inventory.quantity_on_hand - inventory.quantity_reserved
        ),
    )
