from app.features.ai.context import AIToolContext
from app.features.ai.tools.product import create_product_langchain_tools


def test_product_tool_schemas():

    context = AIToolContext(
        db=None,
        current_user=None,
    )

    tools = create_product_langchain_tools(context)

    for product_tool in tools:
        print("\nTool:", product_tool.name)
        print("Description:", product_tool.description)
        print("Arguments:", product_tool.args)


if __name__ == "__main__":
    test_product_tool_schemas()