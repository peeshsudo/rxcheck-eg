"""
FastAPI application entry point.

Changes from prior version:
- Security headers middleware
- Admin endpoints gated by X-Admin-Key
- /docs and /redoc only in development
- Explicit CORS method allowlist (no wildcards)
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine
from app.security import add_security_headers, require_admin_key
from app.routers import (
    drugs,
    products,
    interactions,
    schedules,
    assistant,
    admin,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    # Interactive docs only in development — never expose in production
    docs_url = "/docs" if not settings.is_production else None
    redoc_url = "/redoc" if not settings.is_production else None
    openapi_url = "/openapi.json" if not settings.is_production else None

    app = FastAPI(
        title="RxCheck EG API",
        version="0.2.0",
        description="Drug interaction checker for Egypt. Bilingual AR/EN.",
        lifespan=lifespan,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    # ==== Middleware ====
    app.middleware("http")(add_security_headers)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Admin-Key"],
    )

    # ==== Routers ====
    app.include_router(drugs.router, prefix="/api/v1/drugs", tags=["drugs"])
    app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
    app.include_router(
        interactions.router, prefix="/api/v1/interactions", tags=["interactions"]
    )
    app.include_router(
        schedules.router, prefix="/api/v1/schedules", tags=["schedules"]
    )
    app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["assistant"])

    # Admin routes: require X-Admin-Key on every request
    app.include_router(
        admin.router,
        prefix="/api/v1/admin",
        tags=["admin"],
        dependencies=[Depends(require_admin_key)],
    )

    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "service": "rxcheck-eg",
            "environment": settings.environment,
        }

    return app


app = create_app()