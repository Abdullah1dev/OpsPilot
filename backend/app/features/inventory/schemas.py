from pydantic import BaseModel, ConfigDict, Field
from pydantic import model_validator

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
    quantity: int = Field(ge=0)
    notes: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_movement_quantity(self):
        if (
            self.movement_type != InventoryMovementType.ADJUSTMENT
            and self.quantity <= 0
        ):
            raise ValueError(
                "Receipt and issue quantities must be greater than zero."
            )

        return self
    





class InventoryMovementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inventory_id: int
    movement_type: InventoryMovementType
    quantity: int
    performed_by: int
    notes: str | None
    created_at: datetime


