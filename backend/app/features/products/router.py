from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.auth.models import User
from app.features.products.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.features.products.service import (
    create_product,
    get_product_by_id,
    get_products,
    update_product,
)
from app.infrastructure.database.session import get_db
from app.shared.security.authorization import require_permission
from app.shared.security.permissions import Permission


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_endpoint(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission(Permission.CREATE_PRODUCTS)
    ),
):
    try:
        return create_product(db, product_data, current_user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The product conflicts with an existing database record.",
        ) from exc


@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission(Permission.VIEW_PRODUCTS)
    ),
):
    return get_products(db, current_user)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission(Permission.VIEW_PRODUCTS)
    ),
):
    product = get_product_by_id(db, product_id, current_user)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission(Permission.UPDATE_PRODUCTS)
    ),
):
    try:
        product = update_product(
            db,
            product_id,
            product_data,
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The product conflicts with an existing database record.",
        ) from exc

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product
