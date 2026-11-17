
from langchain_core.messages import AIMessage, HumanMessage

from app.infrastructure.database.session import SessionLocal
from app.features.auth.models import User
from app.features.ai.context import AIToolContext
from app.features.ai.inventory_agent.graph import create_inventory_graph


db = SessionLocal()

try:
    user = db.query(User).filter(
        User.id == 5,
        User.is_active == True,
    ).first()

    if user is None:
        raise RuntimeError("Active test user not found")

    context = AIToolContext(
        db=db,
        current_user=user,
    )

    graph = create_inventory_graph(context)

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="How many Samsung units do we have?"
                )
            ]
        }
    )

    print("\n--- Inventory Agent Response ---")

    for message in result["messages"]:
        print(f"\n{message.type}: {message.content}")

        if isinstance(message, AIMessage) and message.tool_calls:
            print("Tool calls:", message.tool_calls)
        

finally:
    db.close()
