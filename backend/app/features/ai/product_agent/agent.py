from langchain_core.messages import SystemMessage

from app.features.ai.context import AIToolContext
from app.features.ai.llm.client import get_llm
from app.features.ai.tools.product import create_product_langchain_tools


PRODUCT_AGENT_PROMPT = """
You are the Product Specialist Agent for OpsPilot,
an AI operations platform for wholesale and distribution.

Your responsibility is to answer questions about the product catalog.

You have access to these tools:

1. get_products:
   Use for listing products or searching by name, brand, or category.
   You can combine multiple filters when appropriate.

2. get_product_by_sku:
   Use when the user provides a product SKU.

3. get_product_by_id:
   Use when the user explicitly provides a product ID.

Rules:

- Always use the appropriate tool for product information.
- Never invent product information.
- Only report information returned by the tools.
- If no products are found, clearly tell the user.
- If a tool returns an error, explain it clearly and politely.
- Do not answer questions about stock quantities or inventory movements.
- Do not attempt to create, update, or delete products.
- If a question is outside your responsibility, politely explain
  that it should be handled by the appropriate specialist.
"""


def create_product_agent(context: AIToolContext):

    llm = get_llm()

    tools = create_product_langchain_tools(context)

    llm_with_tools = llm.bind_tools(tools)

    def agent(state):
        messages = [
            SystemMessage(content=PRODUCT_AGENT_PROMPT),
            *state["messages"],
        ]

        response = llm_with_tools.invoke(messages)

        return {"messages": [response]}

    return agent
