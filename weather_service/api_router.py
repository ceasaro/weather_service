from fastapi import APIRouter
from .weather_service_app.endpoints import router as weather_service_app_router

router = APIRouter()

router.include_router(
    weather_service_app_router, prefix="/weather_service_app"
)
