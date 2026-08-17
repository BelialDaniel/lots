from contextlib import asynccontextmanager
from core.database import engine
from sqlalchemy import text
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from api.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    yield


app = FastAPI(
    title="Users Management API",
    description="User profiles and configuration service",
    version="0.0.1",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/v1/users/openapi.json",
)

app.include_router(users_router)


@app.get("/api/v1/users/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url="/api/v1/users/openapi.json",
        title=app.title,
    )


@app.get("/api/v1/users/health")
def health_check():
    return {"status": "ok"}
