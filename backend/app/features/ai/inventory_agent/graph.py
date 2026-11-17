from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition

from app.features.ai.context import AIToolContext
from app.features.ai.inventory_agent.state import InventoryAgentState
from app.features.ai.inventory_agent.agent import create_inventory_agent
from app.features.ai.inventory_agent.tool_node import (
    create_inventory_tool_node,
)


def create_inventory_graph(context: AIToolContext):

    agent_node = create_inventory_agent(context)
    tool_node = create_inventory_tool_node(context)

    builder = StateGraph(InventoryAgentState)

    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")

    builder.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )

    builder.add_edge("tools", "agent")

    return builder.compile()
