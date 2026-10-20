import pytest
from sqlalchemy.exc import IntegrityError

from app.features.products.models import Product
from app.features.inventory.models import Inventory
from app.infrastructure.database.session import SessionLocal


@pytest.fixture
def db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_create_product_and_inventory(db):
    product = Product(
        name="Test Laptop Repeatable",
        sku="TEST-LAPTOP-REPEATABLE-001",
        description="Test product for inventory",
        brand="Test Brand",
        category="Laptop",
    )

    db.add(product)
    db.flush()

    inventory = Inventory(
        product_id=product.id,
        quantity_on_hand=100,
        quantity_reserved=20,
    )

    db.add(inventory)
    db.flush()

    assert product.id is not None
    assert inventory.id is not None
    assert inventory.product_id == product.id
    assert inventory.quantity_on_hand == 100
    assert inventory.quantity_reserved == 20


def test_reserved_quantity_cannot_exceed_stock(db):
    product = Product(
        name="Constraint Test Product Repeatable",
        sku="CONSTRAINT-TEST-REPEATABLE-001",
        brand="Test Brand",
        category="Laptop",
    )

    db.add(product)
    db.flush()

    inventory = Inventory(
        product_id=product.id,
        quantity_on_hand=10,
        quantity_reserved=12,
    )

    db.add(inventory)

    with pytest.raises(IntegrityError):
        db.flush()

