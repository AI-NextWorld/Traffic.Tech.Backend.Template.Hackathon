"""Health (ping) routes."""

from fastapi import APIRouter

from app.domain.services.health_service import ping as ping_service
from app.schemas.health import PingResponse


router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get(
    "/ping",
    response_model=PingResponse,
    summary="Health check ping",
    description="Simple endpoint to verify the service is responsive.",
)
def ping() -> PingResponse:
    """Return a basic payload to verify the service is alive."""
    return PingResponse(status="ok", message=ping_service())
