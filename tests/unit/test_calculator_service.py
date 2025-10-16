"""Parameterized unit tests for CalculatorService.

Also includes minimal API tests to cover route wiring and dependencies.
"""

import json
import sys
import math
from pathlib import Path

import pytest

from fastapi.testclient import TestClient

from app.domain.services.calculator_service import CalculatorService


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "tests"/ "integration" / "data"


def load_cases(name: str):
    """Load the JSON dataset for the given operation name."""
    with (DATA_DIR / f"{name}.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def _is_number(x):
    """True if `x` is numeric (int/float) and not a bool."""
    return isinstance(x, (int, float)) and not isinstance(x, bool)


@pytest.fixture(name="calc_service", scope="module")
def _calc_service():
    """CalculatorService instance for tests."""
    return CalculatorService()


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (c["a"], c["b"], c["expected"])
        for c in load_cases("add")
        if "expected" in c and _is_number(c.get("a")) and _is_number(c.get("b"))
    ],
)
def test_add_param(calc_service, a, b, expected):
    """Validate addition using dataset cases."""
    assert math.isclose(calc_service.add(a, b), expected, rel_tol=1e-9)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (c["a"], c["b"], c["expected"])
        for c in load_cases("subtract")
        if "expected" in c and _is_number(c.get("a")) and _is_number(c.get("b"))
    ],
)
def test_subtract_param(calc_service, a, b, expected):
    """Validate subtraction using dataset cases."""
    assert math.isclose(calc_service.subtract(a, b), expected, rel_tol=1e-12)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (c["a"], c["b"], c["expected"])
        for c in load_cases("multiply")
        if "expected" in c and _is_number(c.get("a")) and _is_number(c.get("b"))
    ],
)
def test_multiply_param(calc_service, a, b, expected):
    """Validate multiplication using dataset cases."""
    assert math.isclose(calc_service.multiply(a, b), expected, rel_tol=1e-9)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (c["a"], c["b"], c["expected"])
        for c in load_cases("divide")
        if "expected" in c and _is_number(c.get("a")) and _is_number(c.get("b")) and c.get("b") != 0
    ],
)
def test_divide_param(calc_service, a, b, expected):
    """Validate division using dataset cases (b != 0)."""
    assert math.isclose(calc_service.divide(a, b), expected, rel_tol=1e-9)


@pytest.mark.parametrize(
    "a,b",
    [
        (c.get("a"), c.get("b"))
        for c in load_cases("divide")
        if c.get("b") == 0
    ],
)
def test_divide_by_zero_raises(calc_service, a, b):
    """Division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc_service.divide(a, b)


def test_dependencies_provider_returns_service():
    """Exercise the dependency provider directly."""
    # Asegurar que src esté en sys.path antes del import
    project_root = Path(__file__).resolve().parents[2]
    src_path = project_root / "src" 
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    # Importar localmente para evitar fallos si sys.path aún no fue ajustado
    from app.api.dependencies import get_calculator_service  # type: ignore

    service = get_calculator_service()
    assert isinstance(service, CalculatorService)
    assert service.add(1, 2) == 3


def test_ping_and_calculator_endpoints_minimal():
    """Exercise ping and calculator endpoints to cover main routes."""
    # Asegurar que src esté en sys.path antes del import
    project_root = Path(__file__).resolve().parents[2]
    src_path = project_root / "src" 
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    # Importar localmente para evitar fallos si sys.path aún no fue ajustado
    from main import create_app  # type: ignore

    app = create_app()
    client = TestClient(app)

    # Global ping
    resp = client.get("/api/v1/ping")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "message": "pong"}

    # Calculator router-specific ping
    calc_ping = client.get("/api/v1/calculator/ping")
    assert calc_ping.status_code == 200
    assert calc_ping.json() == {"status": "ok", "message": "pong"}

    # Happy paths
    cases = (
        ("/api/v1/calculator/add", {"a": 1, "b": 2}, 200, 3),
        ("/api/v1/calculator/subtract", {"a": 5, "b": 3}, 200, 2),
        ("/api/v1/calculator/multiply", {"a": 4, "b": 2.5}, 200, 10.0),
        ("/api/v1/calculator/divide", {"a": 9, "b": 3}, 200, 3.0),
    )
    for path, payload, status, expected in cases:
        r = client.post(path, json=payload)
        assert r.status_code == status
        assert r.json() == {"result": expected}

    # Error path: divide by zero
    err = client.post("/api/v1/calculator/divide", json={"a": 1, "b": 0})
    assert err.status_code == 400
    assert err.json().get("detail") == "No se puede dividir por cero"
