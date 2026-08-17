from contextlib import asynccontextmanager
from core.database import engine
from sqlalchemy import text
from fastapi import FastAPI
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
)

app.include_router(users_router)

@app.get("/api/v1/users/health")
def health_check():
    return {"status": "ok"}
