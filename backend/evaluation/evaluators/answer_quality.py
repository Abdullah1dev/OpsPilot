
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
    tool_result: dict,
    final_response: str,
    answer_requirements: list[str],
) -> AnswerQualityResult:

    llm = get_llm()

    judge = llm.with_structured_output(AnswerQualityResult)

    system_prompt = """
    You are an evaluator assessing the final answer of an AI
    inventory assistant.

    Evaluate the answer using ONLY the provided user query,
    tool result, and answer requirements.

    Evaluation rules:

    1. Check whether the answer addresses the user's question.
    2. Verify that all reported facts agree with the tool result.
    3. Check whether the answer satisfies the answer requirements.
    4. Penalize invented quantities, product details, or claims.
    5. If the tool returned an error, check that the answer
       communicates the error accurately.
    6. Do not require exact wording. Different wording is acceptable
       if the meaning and facts are correct.

    Scoring:
    5 = Fully correct, complete, and clear.
    4 = Correct with minor omissions or presentation issues.
    3 = Partially correct, with meaningful omissions.
    2 = Major factual or relevance problems.
    1 = Incorrect, misleading, or fabricated.

    Set passed to true only when the answer is factually correct
    and satisfies the important answer requirements.

    Be strict about factual correctness. Never assume information
    that is not present in the tool result.
    """

    human_prompt = f"""
    USER QUERY:
    {query}

    ACTUAL TOOL RESULT:
    {tool_result}

    FINAL AGENT RESPONSE:
    {final_response}

    ANSWER REQUIREMENTS:
    {answer_requirements}

    Evaluate the final agent response.
    """

    result = judge.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt),
    ])

    return result
