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

    except ValueError as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                type=ToolErrorType.TOOL_ERROR,
                message=str(exc),
            ),
        )