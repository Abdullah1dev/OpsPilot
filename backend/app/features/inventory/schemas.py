from pydantic import BaseModel, ConfigDict


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    sku: str

    quantity_on_hand: int
    quantity_reserved: int
    quantity_available: int