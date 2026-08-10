from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Sistema avançado de monitoramento, "
        "análise e inteligência de criptomoedas."
    ),
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
