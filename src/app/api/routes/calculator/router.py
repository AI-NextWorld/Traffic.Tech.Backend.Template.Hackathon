"""Calculator routes.

Includes basic arithmetic operations and a health ping under the
`/api/v1/calculator` prefix.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_calculator_service
from app.domain.interfaces.calculator_service import ICalculatorService
from app.schemas.calculator import Operands, Result
from app.domain.services.health_service import ping as ping_service
from app.schemas.health import PingResponse


router = APIRouter(prefix="/api/v1/calculator", tags=["calculator"])


@router.get(
    "/ping",
    response_model=PingResponse,
    summary="Health check ping",
    description="Simple endpoint to verify the service is responsive.", 
)
def ping() -> PingResponse:
    """Return a health message for the calculator resource."""
    return PingResponse(status="ok", message=ping_service())


@router.post("/add", response_model=Result)
def add_numbers(
    request: Operands,
    service: ICalculatorService = Depends(get_calculator_service),
) -> Result:
    """Add two operands and return the result."""
    result = service.add(request.a, request.b)
    return Result(result=result)


@router.post("/subtract", response_model=Result)
def substract_numbers(
    request: Operands,
    service: ICalculatorService = Depends(get_calculator_service),
) -> Result:
    """Subtract two operands and return the result."""
    result = service.subtract(request.a, request.b)
    return Result(result=result)


@router.post("/multiply", response_model=Result)
def multiply_numbers(
    request: Operands,
    service: ICalculatorService = Depends(get_calculator_service),
) -> Result:
    """Multiply two operands and return the result."""
    result = service.multiply(request.a, request.b)
    return Result(result=result)


@router.post("/divide", response_model=Result)
def divide_numbers(
    request: Operands,
    service: ICalculatorService = Depends(get_calculator_service),
) -> Result:
    """Divide two operands and return the result (400 if b == 0)."""
    try:
        result = service.divide(request.a, request.b)
    except ZeroDivisionError as exc:
        raise HTTPException(status_code=400, detail="No se puede dividir por cero") from exc
    return Result(result=result)
