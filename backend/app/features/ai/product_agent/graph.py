from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from langchain_core.runnables import RunnableLambda

from app.features.ai.context import AIToolContext
from app.features.ai.product_agent.state import ProductAgentState
from app.features.ai.product_agent.agent import create_product_agent
from app.features.ai.product_agent.tool_node import create_product_tool_node


def create_product_graph(context: AIToolContext):

    agent = create_product_agent(context)
    tool_node = create_product_tool_node(context)

    builder = StateGraph(ProductAgentState)

    builder.add_node("agent", agent)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")

    builder.add_conditional_edges(
        "agent",
        tools_condition,
    )

    builder.add_edge("tools", "agent")

    return builder.compile()
