from langchain_core.tools import tool

from app.features.ai.context import AIToolContext
from app.features.ai.adapters.product import (
    get_products_tool,
    get_product_by_sku_tool,
    get_product_by_id_tool,
)


def create_product_langchain_tools(context: AIToolContext):

    @tool
    def get_products(
        name: str | None = None,
        brand: str | None = None,
        category: str | None = None,
    ) -> dict:
        """
        Retrieve products from the catalog.

        Use this tool to list products or filter them by
        product name, brand, or category.

        Do not use this tool for inventory quantities
        or inventory movement history.
        """
        result = get_products_tool(
            context=context,
            name=name,
            brand=brand,
            category=category,
        )
        return result.model_dump()

    @tool
    def get_product_by_sku(sku: str) -> dict:
        """
        Retrieve a single product using its exact unique SKU.

        Use this when the user provides a product SKU.
        """
        result = get_product_by_sku_tool(
            context=context,
            sku=sku,
        )
        return result.model_dump()

    @tool
    def get_product_by_id(product_id: int) -> dict:
        """
        Retrieve a single product using its database ID.

        Use this when the user explicitly asks about a product ID.
        """
        result = get_product_by_id_tool(
            context=context,
            product_id=product_id,
        )
        return result.model_dump()

    return [
        get_products,
        get_product_by_sku,
        get_product_by_id,
    ]
