from langgraph.prebuilt import ToolNode

from app.features.ai.context import AIToolContext
from app.features.ai.tools.inventory import create_inventory_langchain_tool


def create_inventory_tool_node(context: AIToolContext):
    inventory_tool = create_inventory_langchain_tool(context)

    return ToolNode([inventory_tool])