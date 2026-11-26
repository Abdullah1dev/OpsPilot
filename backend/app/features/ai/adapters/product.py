from app.features.ai.context import AIToolContext
from app.features.ai.schemas import ToolError, ToolErrorType, ToolResult
from app.features.products.schemas import ProductResponse
from app.features.products.service import (
    get_products,
    get_product_by_sku,
    get_product_by_id,
)


def _product_error(
    error_type: ToolErrorType,
    message: str,
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            type=error_type,
            message=message,
        ),
    )


def get_products_tool(
    context: AIToolContext,
    name: str | None = None,
    brand: str | None = None,
    category: str | None = None,
) -> ToolResult:
    try:
        products = get_products(
            db=context.db,
            current_user=context.current_user,
            name=name,
            brand=brand,
            category=category,
        )

        return ToolResult(
            success=True,
            data=[
                ProductResponse.model_validate(product).model_dump(mode="json")
                for product in products
            ],
        )

    except PermissionError:
        return _product_error(
            ToolErrorType.PERMISSION_DENIED,
            "You do not have permission to view products.",
        )

    except Exception:
        return _product_error(
            ToolErrorType.TOOL_ERROR,
            "An unexpected error occurred while retrieving products.",
        )


def get_product_by_sku_tool(
    context: AIToolContext,
    sku: str,
) -> ToolResult:
    try:
        product = get_product_by_sku(
            db=context.db,
            sku=sku,
            current_user=context.current_user,
        )

        if product is None:
            return _product_error(
                ToolErrorType.PRODUCT_NOT_FOUND,
                "No product was found with the provided SKU.",
            )

        return ToolResult(
            success=True,
            data=ProductResponse.model_validate(product).model_dump(mode="json"),
        )

    except PermissionError:
        return _product_error(
            ToolErrorType.PERMISSION_DENIED,
            "You do not have permission to view products.",
        )

    except Exception:
        return _product_error(
            ToolErrorType.TOOL_ERROR,
            "An unexpected error occurred while retrieving the product.",
        )


def get_product_by_id_tool(
    context: AIToolContext,
    product_id: int,
) -> ToolResult:
    try:
        product = get_product_by_id(
            db=context.db,
            product_id=product_id,
            current_user=context.current_user,
        )

        if product is None:
            return _product_error(
                ToolErrorType.PRODUCT_NOT_FOUND,
                "No product was found with the provided ID.",
            )

        return ToolResult(
            success=True,
            data=ProductResponse.model_validate(product).model_dump(mode="json"),
        )

    except PermissionError:
        return _product_error(
            ToolErrorType.PERMISSION_DENIED,
            "You do not have permission to view products.",
        )

    except Exception:
        return _product_error(
            ToolErrorType.TOOL_ERROR,
            "An unexpected error occurred while retrieving the product.",
        )
