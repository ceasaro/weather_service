from typing import Optional
from uuid import UUID

from weather_service.utils.util import APIModel, DateTimeInMillis


class WeatherServiceObjectBase(APIModel):
    name: str


class WeatherServiceObjectDTO(WeatherServiceObjectBase):
    uuid: UUID
    created: Optional[DateTimeInMillis]


class CreateWeatherServiceObject(WeatherServiceObjectBase):
    pass
