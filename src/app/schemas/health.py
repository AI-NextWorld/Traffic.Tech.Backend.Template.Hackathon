"""Schemas for health endpoints."""

from pydantic import BaseModel


class PingResponse(BaseModel):
    """Response model for the health ping."""

    status: str = "ok"
    message: str = "pong"
