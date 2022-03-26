from django.db import models

from weather_service.util import BaseModel


class WeatherServiceObject(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} {self.created}"
