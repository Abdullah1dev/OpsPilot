from app.features.products.models import Product
from app.features.inventory.models import Inventory
from app.infrastructure.database.session import SessionLocal


def test_create_product_and_inventory():
    db = SessionLocal()

    try:
        product = Product(
            name="Test Laptop",
            sku="TEST-LAPTOP-001",
            description="Test product for inventory",
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        inventory = Inventory(
            product_id=product.id,
            quantity_on_hand=100,
            quantity_reserved=20,
        )

        db.add(inventory)
        db.commit()
        db.refresh(inventory)

        assert product.id is not None
        assert inventory.id is not None
        assert inventory.product_id == product.id
        assert inventory.quantity_on_hand == 100
        assert inventory.quantity_reserved == 20

    finally:
        db.close()