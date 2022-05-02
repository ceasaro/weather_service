from django.contrib.gis.db import models

from weather_service.weather_service_app.models.abstact import BaseModel


class Provider(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} {self.created}"


class WeatherStation(BaseModel):
    name = models.CharField(max_length=255)
    location = models.PointField(srid=4326)
    data_provider = models.ForeignKey(Provider, blank=True, null=True, related_name='stations',
                                      on_delete=models.SET_NULL)
