from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.inventory.models import Inventory, InventoryMovement
from app.features.inventory.schemas import (
    InventoryMovementCreate,
    InventoryMovementResponse,
    InventoryResponse,
)
from app.features.products.models import Product
from app.shared.enums.inventory_movement import InventoryMovementType
from app.features.auth.models import User
from app.shared.security.authorization import check_permission
from app.shared.security.permissions import Permission


def get_inventory_by_product_name(
    db: Session,
    product_name: str,
    current_user: User,
) -> InventoryResponse | None:
    check_permission(current_user, Permission.VIEW_INVENTORY)

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



