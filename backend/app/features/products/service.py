from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.auth.models import User
from app.features.products.models import Product
from app.features.products.schemas import ProductCreate, ProductUpdate
from app.shared.security.authorization import check_permission
from app.shared.security.permissions import Permission


def create_product(
    db: Session,
    product_data: ProductCreate,
    current_user: User,
) -> Product:
    check_permission(current_user, Permission.CREATE_PRODUCTS)

    product = Product(**product_data.model_dump())

    try:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    except IntegrityError as exc:
        db.rollback()

        # The SKU is unique, so a duplicate SKU violates a database constraint.
        existing_product = db.scalar(
            select(Product).where(Product.sku == product_data.sku)
        )

        if existing_product is not None:
            raise ValueError("A product with this SKU already exists.") from exc

        raise


def get_products(
    db: Session,
    current_user: User,
) -> list[Product]:
    check_permission(current_user, Permission.VIEW_PRODUCTS)

    statement = select(Product).order_by(Product.id)
    return list(db.scalars(statement).all())


def get_product_by_id(
    db: Session,
    product_id: int,
    current_user: User,
) -> Product | None:
    check_permission(current_user, Permission.VIEW_PRODUCTS)

    return db.get(Product, product_id)


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
    current_user: User,
) -> Product | None:
    check_permission(current_user, Permission.UPDATE_PRODUCTS)

    product = db.get(Product, product_id)

    if product is None:
        return None

    update_data = product_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    try:
        db.commit()
        db.refresh(product)
        return product

    except IntegrityError as exc:
        db.rollback()

        # A SKU update may conflict with another product's SKU.
        if "sku" in update_data:
            existing_product = db.scalar(
                select(Product).where(Product.sku == update_data["sku"])
            )

            if existing_product is not None:
                raise ValueError(
                    "A product with this SKU already exists."
                ) from exc

        raise
