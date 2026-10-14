
from fastapi import FastAPI

from app.core.config import settings
from app.features.auth.router import router as auth_router


app = FastAPI(
    title=settings.app_name,
    description="AI Operations Platform for Wholesale & Distribution",
    version="0.1.0",
)

app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }
