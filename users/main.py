from contextlib import asynccontextmanager
import models  # noqa: F401
from core.database import engine
from sqlalchemy import text
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from api.errors import persistence_error_handler
from api.users import router as users_router
from api.developers import router as developers_router
from api.internal import router as internal_router
from services.auth_verify import close_auth_client, init_auth_client
from services.persistence import PersistenceError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_auth_client()
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await close_auth_client()


app = FastAPI(
    title="Users Management API",
    description="User profiles and configuration service",
    version="0.0.1",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/v1/users/openapi.json",
)

app.add_exception_handler(PersistenceError, persistence_error_handler)
app.include_router(users_router)
app.include_router(developers_router)
app.include_router(internal_router)


@app.get("/api/v1/users/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url="/api/v1/users/openapi.json",
        title=app.title,
    )


@app.get("/api/v1/users/health")
def health_check():
    return {"status": "ok"}
