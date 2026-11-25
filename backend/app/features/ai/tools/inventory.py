from app.features.ai.context import AIToolContext
from app.features.ai.adapters.inventory import get_inventory_tool
from langchain_core.tools import tool




def create_inventory_langchain_tool(context: AIToolContext):
    @tool
    def get_inventory(
        product_name: str | None = None,
        sku: str | None = None,
    ) -> dict:
        """Retrieve current stock for a product by its name, SKU, or both.
        Use this for questions about quantity on hand, reserved stock,
        and available stock. If the product name is ambiguous, provide
        its SKU when available. Do not use this tool for movement history
        or general product catalog searches.
        """
        result = get_inventory_tool(
            context=context,
            product_name=product_name,
            sku=sku,
        )

        return result.model_dump()

    return get_inventory
