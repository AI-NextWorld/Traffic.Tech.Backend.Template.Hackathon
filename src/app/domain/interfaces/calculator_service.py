"""Domain interfaces (protocols) for calculator services."""

from typing import Protocol


class ICalculatorService(Protocol):
    """Contract for basic arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        """Add two values."""

    def subtract(self, a: float, b: float) -> float:
        """Subtract the second value from the first."""

    def multiply(self, a: float, b: float) -> float:
        """Multiply two values."""

    def divide(self, a: float, b: float) -> float:
        """Divide the first value by the second."""
