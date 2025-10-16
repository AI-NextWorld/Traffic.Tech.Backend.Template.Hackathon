"""Pruebas unitarias para el servicio de salud (ping)."""

from app.domain.services.health_service import ping


def test_ping_returns_pong():
    """El servicio debe retornar 'pong'."""
    assert ping() == "pong"
