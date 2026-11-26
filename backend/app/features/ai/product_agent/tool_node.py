
from langgraph.prebuilt import ToolNode

from app.features.ai.context import AIToolContext
from app.features.ai.tools.product import create_product_langchain_tools


def create_product_tool_node(context: AIToolContext):

    tools = create_product_langchain_tools(context)

    return ToolNode(tools)
