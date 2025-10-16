"""Input/output schemas for calculator operations."""

from typing import Union

from pydantic import BaseModel, Field, StrictFloat, StrictInt


class Operands(BaseModel):
    """Pair of strict numeric operands."""

    # Accepts only strict numbers (int or float), no coercion from strings
    a: Union[StrictInt, StrictFloat] = Field(..., description="First operand")
    b: Union[StrictInt, StrictFloat] = Field(..., description="Second operand")


class Result(BaseModel):
    """Response model with the operation result."""

    result: float
