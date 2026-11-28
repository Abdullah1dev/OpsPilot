from langchain_core.messages import AIMessage, HumanMessage

from app.infrastructure.database.session import SessionLocal
from app.features.auth.models import User
from app.features.ai.context import AIToolContext
from app.features.ai.product_agent.graph import create_product_graph


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

    graph = create_product_graph(context)

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="Show me the inventory movement history for Samsung."
                )
            ]
        }
    )

    print("\n--- Product Agent Response ---")

    for message in result["messages"]:
        print(f"\n{message.type}: {message.content}")

        if isinstance(message, AIMessage) and message.tool_calls:
            print("Tool calls:", message.tool_calls)

finally:
    db.close()
