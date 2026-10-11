from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI Operations Platform for Wholesale & Distribution",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }