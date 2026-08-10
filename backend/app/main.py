from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.database import engine
from app.models.asset import Base


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )

    yield

    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Sistema avançado de monitoramento, "
        "análise e inteligência de criptomoedas."
    ),
    lifespan=lifespan,
)


@app.get("/")
async def root():

    return {
        "project": settings.app_name,
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "service": "api",
    }
