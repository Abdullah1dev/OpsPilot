
import pytest

from app.features.auth.models import User
from app.features.products.models import Product
from app.features.inventory.models import Inventory
from app.features.inventory.service import get_inventory_by_product_name
from app.infrastructure.database.session import SessionLocal
from app.shared.enums.roles import UserRole


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def current_user():
    return User(
        id=1,
        email="manager@example.com",
        hashed_password="test-hash",
        role=UserRole.MANAGER,
        is_active=True,
    )


def test_get_inventory_by_product_name(db, current_user):
    product = Product(
        name="Service Test Laptop",
        sku="SERVICE-TEST-LAPTOP-001",
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

    result = get_inventory_by_product_name(
        db,
        "Service Test Laptop",
        current_user,
    )

    assert result is not None
    assert result.product_name == "Service Test Laptop"
    assert result.quantity_on_hand == 100
    assert result.quantity_reserved == 20
    assert result.quantity_available == 80


def test_get_inventory_for_nonexistent_product(db, current_user):
    result = get_inventory_by_product_name(
        db,
        "Product That Does Not Exist 12345",
        current_user,
    )

    assert result is None
