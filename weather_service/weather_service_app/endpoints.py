from typing import List

from fastapi import APIRouter

from .models import WeatherServiceObject
from .schemas import WeatherServiceObjectDTO, CreateWeatherServiceObject

router = APIRouter()


@router.get("/", response_model=List[WeatherServiceObjectDTO])
def get_weather_service_app() -> List[WeatherServiceObject]:
    query = WeatherServiceObject.objects.all()
    return list(query)


@router.post("/", status_code=201, response_model=WeatherServiceObjectDTO)
def create_weather_service_object(request: CreateWeatherServiceObject):
    return WeatherServiceObject.objects.create(name=request.name)
