from app.features.ai.context import AIToolContext
from app.features.ai.schemas import ToolError, ToolErrorType, ToolResult
from app.features.inventory.service import get_inventory


def get_inventory_tool(
    context: AIToolContext,
    product_name: str | None = None,
    sku: str | None = None,
) -> ToolResult:
    try:
        inventory = get_inventory(
            db=context.db,
            current_user=context.current_user,
            product_name=product_name,
            sku=sku,
        )

        return ToolResult(
            success=True,
            data=inventory.model_dump(),
        )

    except PermissionError:
        return ToolResult(
            success=False,
            error=ToolError(
                type=ToolErrorType.PERMISSION_DENIED,
                message="You do not have permission to view inventory.",
            ),
        )

    except ValueError as exc:
        message = str(exc)

        if message == "No product matches the provided identifier(s).":
            error_type = ToolErrorType.PRODUCT_NOT_FOUND

        elif message.startswith("Multiple products match"):
            error_type = ToolErrorType.AMBIGUOUS_PRODUCT

        else:
            error_type = ToolErrorType.VALIDATION_ERROR

        return ToolResult(
            success=False,
            error=ToolError(
                type=error_type,
                message=message,
            ),
        )

    except Exception:
        return ToolResult(
            success=False,
            error=ToolError(
                type=ToolErrorType.TOOL_ERROR,
                message="An unexpected error occurred while retrieving inventory.",
            ),
        )