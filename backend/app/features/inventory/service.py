from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.auth.models import User
from app.features.inventory.models import Inventory, InventoryMovement
from app.features.inventory.schemas import (
    InventoryMovementCreate,
    InventoryMovementResponse,
    InventoryResponse,
)
from app.features.products.models import Product
from app.shared.enums.inventory_movement import InventoryMovementType
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


def record_inventory_movement(
    db: Session,
    product_id: int,
    movement: InventoryMovementCreate,
    current_user: User,
) -> InventoryMovementResponse:
    check_permission(
        current_user,
        Permission.RECORD_INVENTORY_MOVEMENT,
    )

    try:
        statement = (
            select(Inventory)
            .where(Inventory.product_id == product_id)
            .with_for_update()
        )

        inventory = db.execute(statement).scalar_one_or_none()

        if inventory is None:
            raise ValueError(
                "Inventory record not found for this product."
            )

        if movement.movement_type == InventoryMovementType.RECEIPT:
            inventory.quantity_on_hand += movement.quantity

        elif movement.movement_type == InventoryMovementType.ISSUE:
            available_quantity = (
                inventory.quantity_on_hand - inventory.quantity_reserved
            )

            if movement.quantity > available_quantity:
                raise ValueError(
                    "Cannot issue more stock than the available quantity."
                )

            inventory.quantity_on_hand -= movement.quantity

        elif movement.movement_type == InventoryMovementType.ADJUSTMENT:
            if movement.quantity < inventory.quantity_reserved:
                raise ValueError(
                    "Adjusted stock cannot be less than reserved stock."
                )

            inventory.quantity_on_hand = movement.quantity

        inventory_movement = InventoryMovement(
            inventory_id=inventory.id,
            movement_type=movement.movement_type,
            quantity=movement.quantity,
            performed_by=current_user.id,
            notes=movement.notes,
        )

        db.add(inventory_movement)
        db.flush()

        response = InventoryMovementResponse.model_validate(
            inventory_movement
        )

        db.commit()

        return response

    except Exception:
        db.rollback()
        raise
