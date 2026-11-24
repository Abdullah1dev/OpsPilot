
from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage, HumanMessage

from app.features.ai.llm.client import get_llm


class AnswerQualityResult(BaseModel):
    score: int = Field(ge=1, le=5)
    passed: bool
    reasoning: str
    issues: list[str]


def evaluate_answer_quality(
    query: str,
    tool_result: dict | None,
    final_response: str,
    answer_requirements: list[str],
    expected_outcome: str = "success",
) -> AnswerQualityResult:

    llm = get_llm()
    judge = llm.with_structured_output(AnswerQualityResult)

    system_prompt = """
    You are an evaluator assessing the final answer of an AI inventory assistant.

    Evaluate the answer using ONLY the provided user query, tool result,
    expected outcome, and answer requirements.

    General rules:

    1. Check whether the answer addresses the user's question.
    2. Never accept invented quantities, product details, or claims.
    3. Do not require exact wording.
    4. Be strict about factual correctness.

    When expected outcome is success:
    - Verify reported facts against the tool result.
    - Check that the answer satisfies the answer requirements.

    When expected outcome is error:
    - Check that the answer communicates the tool error accurately.
    - Ensure it does not invent quantities or pretend the operation succeeded.

    When expected outcome is not_applicable:
    - Check that the agent recognizes the question is outside its responsibility.
    - Check that it does not pretend to have retrieved the requested information.
    - Check that it does not invent information or use an unrelated tool result.

    Scoring:
    5 = Fully correct, complete, and clear.
    4 = Correct with minor omissions.
    3 = Partially correct.
    2 = Major factual or relevance problems.
    1 = Incorrect, misleading, or fabricated.

    Set passed to true only when the answer is factually correct
    and satisfies the important answer requirements.
    """

    human_prompt = f"""
    USER QUERY:
    {query}

    EXPECTED OUTCOME:
    {expected_outcome}

    ACTUAL TOOL RESULT:
    {tool_result}

    FINAL AGENT RESPONSE:
    {final_response}

    ANSWER REQUIREMENTS:
    {answer_requirements}

    Evaluate the final agent response.
    """

    return judge.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt),
    ])
