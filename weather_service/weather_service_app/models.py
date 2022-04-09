from statistics import mean

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance

from weather_service.util import BaseModel
from weather_service.weather_service_app.exceptions import WeatherServiceModelException

User = settings.AUTH_USER_MODEL


class WeatherServiceObject(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} {self.created}"


class MeasurementConsts:
    AIR_TEMPERATURE = 'AT'
    AIR_TEMPERATURE_AVG = 'AT_AVG'
    AIR_TEMPERATURE_MAX = 'AT_MAX'
    AIR_TEMPERATURE_MIN = 'AT_MIN'
    CLOUD = 'CL'
    EVAPOTRANSPIRATION_DAY = 'ET_DAY'
    LEAF_WETNESS = 'LW'
    PRECIPITATION = 'PT'
    RADIATION = 'RAD'
    RADIATION_SHORTWAVE = 'RAD_SHORT'
    RADIATION_SHORTWAVE_AVG = 'RAD_SHORT_AVG'
    RADIATION_SHORTWAVE_MAX = 'RAD_SHORT_MAX'
    RELATIVE_HUMIDITY = 'RH'
    RELATIVE_HUMIDITY_AVG = 'RH_AVG'
    RELATIVE_HUMIDITY_MAX = 'RH_MAX'
    RELATIVE_HUMIDITY_MIN = 'RH_MIN'
    WIND_DIRECTION = 'WD'  # voor uur data gemiddelde (laatste waarden tonen)
    WIND_SPEED = 'WS'  # voor uur data gemiddelde
    WIND_SPEED_AVG = 'WS_AVG'  # voor uur data gemiddelde
    WIND_SPEED_GUST = 'WS_GUST'
    WIND_SPEED_MAX = 'WS_MAX'  # voor uur data max

    DATA = {
        AIR_TEMPERATURE: {
            'name': 'Air Temperature',
            'unit': u'°C',
            'domain': [-10, 40],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 20,  # the maximum radius from where is was measured where it is still valid to use
        },
        PRECIPITATION: {
            'name': 'Precipitation',
            'unit': 'mm',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': sum,
            'max_reach_radius_km': 10,  # the maximum radius from where is was measured where it is still valid to use
        },
        RADIATION: {
            'name': 'Radiation',
            'unit': u'Watt/m²',
            'domain': [0, 300],  # values outside the domain are considered invalid.
            'group_function': sum,
            'max_reach_radius_km': 50,  # the maximum radius from where is was measured where it is still valid to use
        },
        RADIATION_SHORTWAVE: {
            'name': 'Shortwave radiation',
            'unit': u'W/m²',
            'domain': [0, 300],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 50,  # the maximum radius from where is was measured where it is still valid to use
        },
        RELATIVE_HUMIDITY: {
            'name': 'Relative Humidity',
            'unit': '%',
            'domain': [0, 100],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 20,  # the maximum radius from where is was measured where it is still valid to use
        },
        WIND_DIRECTION: {
            'name': 'Wind Direction',
            'unit': u'°',
            'domain': [0, 360],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 30,  # the maximum radius from where is was measured where it is still valid to use
        },
        WIND_SPEED: {
            'name': 'Wind Speed',
            'unit': 'm/s',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 30,  # the maximum radius from where is was measured where it is still valid to use
        },
        WIND_SPEED_MAX: {
            'name': 'Wind Speed max',
            'unit': 'm/s',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': max,
            'max_reach_radius_km': 30,  # the maximum radius from where is was measured where it is still valid to use
        },
        WIND_SPEED_GUST: {
            'name': 'Wind Speed gust',
            'unit': 'm/s',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': max,
            'max_reach_radius_km': 30,  # the maximum radius from where is was measured where it is still valid to use
        },
    }

    @staticmethod
    def group_meta_by_radius(meta):
        grouped_meta_by_radius = {}
        for _meta in meta:
            meta_data = MeasurementConsts.DATA.get(_meta)
            if not meta_data:
                raise WeatherServiceModelException(f"Unknown measurement meta key '{_meta}'.")

            meta_list = grouped_meta_by_radius.setdefault(meta_data.get('max_reach_radius_km'), [])
            meta_list.append(_meta)
        return grouped_meta_by_radius


class MeasurementQuerySet(models.QuerySet):

    def find(self, location, start_date, end_date, meta):
        grouped_meta = MeasurementConsts.group_meta_by_radius(meta)
        query_set = self.none()
        for radius_in_km, meta_list in grouped_meta.items():
            query_set |= self.filter(measurement_meta__in=meta_list).within_distance(location, radius_in_km)

        query_set = query_set.filter(day__range=(start_date, end_date)).filter(measurement_meta__in=meta)
        return query_set.order_by('day')

    def within_distance(self, location, max_distance_in_km):
        return self.order_by_distance(location).filter(distance__lt=max_distance_in_km * 1000)

    def order_by_distance(self, location):
        return self.distance(location).order_by('distance')

    def distance(self, location):
        return self.annotate(distance=Distance("location", location))


class Measurement(MeasurementConsts, models.Model):
    day = models.DateField()
    location = models.PointField(srid=4326)
    measurement_meta = models.CharField(max_length=20)
    value = models.FloatField()
    data_provider = models.ForeignKey(User, blank=True, null=True, related_name='measurements',
                                      on_delete=models.SET_NULL)

    objects = MeasurementQuerySet.as_manager()

    class Meta:
        ordering = ['day', 'location', 'measurement_meta']
        indexes = [
            models.Index(fields=['day', 'location'], name='day_location_idx'),
        ]

    def __str__(self):
        return f'{self.day} - {self.measurement_meta}'
