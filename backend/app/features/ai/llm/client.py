import os

from langchain_openai import ChatOpenAI


def get_llm() -> ChatOpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not configured.")

    if not model:
        raise ValueError("OPENROUTER_MODEL is not configured.")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        timeout=60,
        max_retries=2,
    )
