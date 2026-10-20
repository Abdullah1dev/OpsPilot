import pytest

from app.features.auth.models import User
from app.features.products.models import Product
from app.features.products.schemas import ProductCreate, ProductUpdate
from app.features.products.service import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
)
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


def make_user(role: UserRole) -> User:
    return User(
        email=f"{role.value.lower()}-product-test@example.com",
        hashed_password="test-hash",
        role=role,
        is_active=True,
    )


def make_product_data(sku="TEST-LAPTOP-001"):
    return ProductCreate(
        name="Test Laptop",
        sku=sku,
        brand="Test Brand",
        category="Laptop",
        description="Product service test",
    )





def test_sales_cannot_create_product(db):
    sales_user = make_user(UserRole.SALES)

    with pytest.raises(PermissionError):
        create_product(
            db,
            make_product_data("SALES-FORBIDDEN-001"),
            sales_user,
        )


def test_can_list_and_get_products(db):
    manager = make_user(UserRole.MANAGER)
    created = create_product(
        db,
        make_product_data("LIST-TEST-001"),
        manager,
    )

    products = get_products(db, manager)
    found = get_product_by_id(db, created.id, manager)

    assert any(product.id == created.id for product in products)
    assert found is not None
    assert found.sku == "LIST-TEST-001"


def test_manager_can_create_product(db):
    manager = make_user(UserRole.MANAGER)

    product = create_product(
        db,
        make_product_data("MANAGER-CREATE-TEST-20261020"),
        manager,
    )

    assert product.id is not None
    assert product.sku == "MANAGER-CREATE-TEST-20261020"
    assert product.name == "Test Laptop"


def test_update_nonexistent_product_returns_none(db):
    manager = make_user(UserRole.MANAGER)

    result = update_product(
        db,
        999999999,
        ProductUpdate(brand="Updated Brand"),
        manager,
    )

    assert result is None


def test_duplicate_sku_is_rejected(db):
    manager = make_user(UserRole.MANAGER)

    create_product(
        db,
        make_product_data("DUPLICATE-TEST-001"),
        manager,
    )

    with pytest.raises(ValueError, match="SKU already exists"):
        create_product(
            db,
            make_product_data("DUPLICATE-TEST-001"),
            manager,
        )
