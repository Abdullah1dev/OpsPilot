import json
from pathlib import Path

from langchain_core.messages import HumanMessage

from app.infrastructure.database.session import SessionLocal
from app.features.auth.models import User
from app.features.ai.context import AIToolContext
from app.features.ai.inventory_agent.graph import create_inventory_graph

from evaluation.evaluators.deterministic import evaluate_inventory_case


DATASET_PATH = (
    Path(__file__).resolve().parent
    / "datasets"
    / "inventory.json"
)


def load_dataset() -> list[dict]:
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    return dataset["cases"]


def run_evaluation() -> list[dict]:
    cases = load_dataset()
    evaluation_results = []

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == 5,
            User.is_active.is_(True),
        ).first()

        if user is None:
            raise RuntimeError("Active test user not found")

        context = AIToolContext(
            db=db,
            current_user=user,
        )

        graph = create_inventory_graph(context)

        for case in cases:
            print(f"\nRunning {case['id']}: {case['query']}")

            try:
                result = graph.invoke(
                    {
                        "messages": [
                            HumanMessage(content=case["query"])
                        ]
                    }
                )

                evaluation = evaluate_inventory_case(
                    case=case,
                    messages=result["messages"],
                )

                evaluation_results.append(evaluation)

                status = "PASS" if evaluation["passed"] else "FAIL"
                print(f"Result: {status}")
                print(f"Checks: {evaluation['checks']}")

            except Exception as exc:
                evaluation_results.append({
                    "case_id": case["id"],
                    "passed": False,
                    "error": str(exc),
                })

                print(f"Execution error: {exc}")

    finally:
        db.close()

    return evaluation_results


if __name__ == "__main__":
    results = run_evaluation()

    total = len(results)
    passed = sum(result["passed"] for result in results)
    failed = total - passed

    print("\n========== EVALUATION SUMMARY ==========")
    print(f"Total cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    print("\nDetailed results:")
    print(json.dumps(results, indent=4))
