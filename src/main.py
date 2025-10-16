"""FastAPI application entry point.

Exposes a factory function `create_app` and a global `app` instance to be
used by ASGI servers such as Uvicorn.
"""

from fastapi import FastAPI

from app.api.routes.calculator.router import router as calculator_router
from app.api.routes.ping import router as ping_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    application = FastAPI(
        title="Traffic Tech Backend Template",
        version="0.1.0",
        description=(
            "Backend template with FastAPI, including calculator and health check.\n\n"
            "Swagger UI available at /docs and OpenAPI at /openapi.json."
        ),
        contact={
            "name": "Traffic Tech",
        },
    )

    # Routes
    application.include_router(ping_router)
    application.include_router(calculator_router)

    return application


app = create_app()
