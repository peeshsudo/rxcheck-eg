from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine
from app.routers import drugs, interactions, products, schedules, assistant, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: warm caches, verify DB connection, etc.
    yield
    # Shutdown: close pools
    await engine.dispose()


app = FastAPI(
    title="RxCheck EG API",
    version="0.1.0",
    description="Drug interaction checker for Egypt. Bilingual AR/EN.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drugs.router, prefix="/api/v1/drugs", tags=["drugs"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(interactions.router, prefix="/api/v1/interactions", tags=["interactions"])
app.include_router(schedules.router, prefix="/api/v1/schedules", tags=["schedules"])
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["assistant"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "rxcheck-eg"}