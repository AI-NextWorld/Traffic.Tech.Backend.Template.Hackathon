"""Domain implementation of the calculator service."""

from app.domain.interfaces.calculator_service import ICalculatorService


class CalculatorService(ICalculatorService):
    """Implements basic arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b
