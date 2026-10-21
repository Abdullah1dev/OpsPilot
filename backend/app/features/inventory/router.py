from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.features.auth.models import User
from app.features.inventory.schemas import (
    InventoryMovementCreate,
    InventoryMovementResponse,
    InventoryResponse,
)
from app.features.inventory.service import (
    get_inventory_by_product_name,
    record_inventory_movement,
)
from app.infrastructure.database.session import get_db
from app.shared.security.authorization import require_permission
from app.shared.security.permissions import Permission

from app.features.inventory.service import get_inventory_movements


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.get(
    "/by-name/{product_name}",
    response_model=InventoryResponse,
    summary="Get inventory by product name",
)
def get_inventory(
    product_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission(Permission.VIEW_INVENTORY)
    ),
) -> InventoryResponse:
    inventory = get_inventory_by_product_name(
        db=db,
        product_name=product_name,
        current_user=current_user,
    )

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product inventory not found.",
        )

    return inventory


@router.post(
    "/{product_id}/movements",
    response_model=InventoryMovementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record an inventory movement",
)
def create_inventory_movement(
    product_id: int,
    movement: InventoryMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission(Permission.RECORD_INVENTORY_MOVEMENT)
    ),
) -> InventoryMovementResponse:
    try:
        return record_inventory_movement(
            db=db,
            product_id=product_id,
            movement=movement,
            current_user=current_user,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "Inventory record not found for this product.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        ) from exc



@router.get(
    "/{product_id}/movements",
    response_model=list[InventoryMovementResponse],
    summary="Get inventory movement history",
)
def get_product_inventory_movements(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission(Permission.VIEW_INVENTORY_MOVEMENTS)
    ),
) -> list[InventoryMovementResponse]:
    return get_inventory_movements(
        db=db,
        product_id=product_id,
        current_user=current_user,
    )