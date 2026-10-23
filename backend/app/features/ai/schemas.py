
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SpecialistType(str, Enum):
    INVENTORY = "inventory"
    PRODUCT = "product"
    MOVEMENT = "movement"
    UNSUPPORTED = "unsupported"


class SupervisorDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    specialist: SpecialistType


class ToolErrorType(str, Enum):
    PRODUCT_NOT_FOUND = "product_not_found"
    AMBIGUOUS_PRODUCT = "ambiguous_product"
    PERMISSION_DENIED = "permission_denied"
    VALIDATION_ERROR = "validation_error"
    TOOL_ERROR = "tool_error"


class ToolError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: ToolErrorType
    message: str = Field(min_length=1)





class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    data: dict | list | None = None
    error: ToolError | None = None

    @model_validator(mode="after")
    def check_result_consistency(self) -> "ToolResult":
        if self.success:
            if self.error is not None or self.data is None:
                raise ValueError(
                    "Successful results require data and cannot contain an error."
                )
        else:
            if self.error is None:
                raise ValueError("Failed results must contain an error.")

            if self.data is not None:
                raise ValueError("Failed results cannot contain data.")

        return self




class AIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    response: str = Field(min_length=1)
    specialist: SpecialistType
    success: bool
