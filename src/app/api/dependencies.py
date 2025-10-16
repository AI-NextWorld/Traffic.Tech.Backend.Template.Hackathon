"""Common dependencies injected into API routes."""

from app.domain.services.calculator_service import CalculatorService
from app.domain.interfaces.calculator_service import ICalculatorService


def get_calculator_service() -> ICalculatorService:
    """Provider of `ICalculatorService` for dependency injection."""
    return CalculatorService()
