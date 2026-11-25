
import json
from pathlib import Path

from langchain_core.messages import HumanMessage

from app.infrastructure.database.session import SessionLocal
from app.features.auth.models import User
from app.features.ai.context import AIToolContext
from app.features.ai.inventory_agent.graph import create_inventory_graph

from evaluation.evaluators.deterministic import evaluate_inventory_case
from evaluation.evaluators.answer_quality import evaluate_answer_quality


DATASET_PATH = (
    Path(__file__).resolve().parent
    / "datasets"
    / "inventory.json"
)


def load_dataset() -> list[dict]:
    """Load inventory evaluation cases from JSON."""
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    return dataset["cases"]


def run_evaluation() -> list[dict]:
    """Run deterministic and answer-quality evaluation."""

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
                # Execute the Inventory Agent
                result = graph.invoke(
                    {
                        "messages": [
                            HumanMessage(content=case["query"])
                        ]
                    }
                )

                # 1. Deterministic evaluation
                deterministic_result = evaluate_inventory_case(
                    case=case,
                    messages=result["messages"],
                )

                # 2. Answer-quality evaluation
                answer_quality_result = None

                tool_result = deterministic_result.get("tool_result")
                final_response = deterministic_result.get("final_response")

                answer_quality_result = None

                tool_result = deterministic_result.get("tool_result")
                final_response = deterministic_result.get("final_response")

                if final_response:
                    answer_quality_result = evaluate_answer_quality(
                        query=case["query"],
                        tool_result=tool_result,
                        final_response=final_response,
                        answer_requirements=case["answer_requirements"],
                        expected_outcome=case["expected_outcome"],
                    )
                    
                    

                # Combine both evaluation results
                evaluation = {
                    "case_id": case["id"],
                    "deterministic": deterministic_result,
                    "answer_quality": (
                        answer_quality_result.model_dump()
                        if answer_quality_result is not None
                        else None
                    ),
                }

                evaluation["passed"] = (
                    deterministic_result["passed"]
                    and answer_quality_result is not None
                    and answer_quality_result.passed
                )

                evaluation_results.append(evaluation)

                # Display results
                status = "PASS" if evaluation["passed"] else "FAIL"

                print(f"Result: {status}")
                print(
                    f"Deterministic: "
                    f"{deterministic_result['passed']}"
                )

                if answer_quality_result is not None:
                    print(
                        f"Answer quality score: "
                        f"{answer_quality_result.score}/5"
                    )
                    print(
                        f"Answer quality passed: "
                        f"{answer_quality_result.passed}"
                    )
                else:
                    print("Answer quality: Not evaluated")

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
