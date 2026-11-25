from unittest.mock import MagicMock

from app.features.ai.context import AIToolContext
from app.features.ai.tools.inventory import create_inventory_langchain_tool


def test_inventory_langchain_tool_creation():

    context = AIToolContext(
        db=MagicMock(),
        current_user=MagicMock(),
    )

    inventory_tool = create_inventory_langchain_tool(context)

    assert inventory_tool.name == "get_inventory"

    assert "product_name" in inventory_tool.args
    assert "sku" in inventory_tool.args

    assert "db" not in inventory_tool.args
    assert "current_user" not in inventory_tool.args