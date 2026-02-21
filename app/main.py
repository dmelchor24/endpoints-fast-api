from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.routers import tasks, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables ready")
    yield

app = FastAPI(title="Task API Async", lifespan=lifespan)

app.include_router(tasks.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")