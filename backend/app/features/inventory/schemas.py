from pydantic import BaseModel, ConfigDict, Field

from app.shared.enums.inventory_movement import InventoryMovementType
from datetime import datetime


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    sku: str

    quantity_on_hand: int
    quantity_reserved: int
    quantity_available: int
    
    


class InventoryMovementCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    movement_type: InventoryMovementType
    quantity: int = Field(gt=0)
    notes: str | None = Field(default=None, max_length=500)
    





class InventoryMovementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inventory_id: int
    movement_type: InventoryMovementType
    quantity: int
    performed_by: int
    notes: str | None
    created_at: datetime


