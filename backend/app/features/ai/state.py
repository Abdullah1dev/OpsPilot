
from typing import TypedDict

from app.features.ai.schemas import SpecialistType


class OpsPilotState(TypedDict):
    user_query: str
    user_id: int

    specialist: SpecialistType | None

    tool_result: dict | list | None
    error: dict | None

    final_response: str | None
