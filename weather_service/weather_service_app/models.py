from datetime import date, datetime, timedelta
from statistics import mean

import pytz
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
    WIND_DIRECTION = 'WD'
    WIND_SPEED = 'WS'
    WIND_SPEED_AVG = 'WS_AVG'
    WIND_SPEED_GUST = 'WS_GUST'
    WIND_SPEED_MAX = 'WS_MAX'

    DATA = {
        AIR_TEMPERATURE: {
            'name': 'Air Temperature',
            'unit': u'°C',
            'domain': [-10, 40],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 20,  # the maximum radius where this value is still valid to use
        },
        PRECIPITATION: {
            'name': 'Precipitation',
            'unit': 'mm',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': sum,
            'max_reach_radius_km': 10,  # the maximum radius where this value is still valid to use
        },
        RADIATION: {
            'name': 'Radiation',
            'unit': u'Watt/m²',
            'domain': [0, 300],  # values outside the domain are considered invalid.
            'group_function': sum,
            'max_reach_radius_km': 50,  # the maximum radius where this value is still valid to use
        },
        RADIATION_SHORTWAVE: {
            'name': 'Shortwave radiation',
            'unit': u'W/m²',
            'domain': [0, 300],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 50,  # the maximum radius where this value is still valid to use
        },
        RELATIVE_HUMIDITY: {
            'name': 'Relative Humidity',
            'unit': '%',
            'domain': [0, 100],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 20,  # the maximum radius where this value is still valid to use
        },
        WIND_DIRECTION: {
            'name': 'Wind Direction',
            'unit': u'°',
            'domain': [0, 360],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 30,  # the maximum radius where this value is still valid to use
        },
        WIND_SPEED: {
            'name': 'Wind Speed',
            'unit': 'm/s',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': mean,
            'max_reach_radius_km': 30,  # the maximum radius where this value is still valid to use
        },
        WIND_SPEED_MAX: {
            'name': 'Wind Speed max',
            'unit': 'm/s',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': max,
            'max_reach_radius_km': 30,  # the maximum radius where this value is still valid to use
        },
        WIND_SPEED_GUST: {
            'name': 'Wind Speed gust',
            'unit': 'm/s',
            'domain': [0, 20],  # values outside the domain are considered invalid.
            'group_function': max,
            'max_reach_radius_km': 30,  # the maximum radius where this value is still valid to use
        },
    }

    @staticmethod
    def group_meta_by_radius(meta_list):
        grouped_meta_by_radius = {}
        for _meta in meta_list:
            meta_data = MeasurementConsts.get_meta_data(_meta)

            meta_list = grouped_meta_by_radius.setdefault(meta_data.get('max_reach_radius_km'), [])
            meta_list.append(_meta)
        return grouped_meta_by_radius

    @staticmethod
    def grouped_value(values, meta):
        if values:
            meta_data = MeasurementConsts.get_meta_data(meta)
            group_function = meta_data.get('group_function')
            return group_function(values)

    @staticmethod
    def get_meta_data(meta):
        meta_data = MeasurementConsts.DATA.get(meta)
        if not meta_data:
            raise WeatherServiceModelException(f"Unknown measurement meta key '{meta}'.")
        return meta_data


class BaseMeasurementQuerySet(models.QuerySet):

    class Meta:
        abstract = True

    def find(self, location, start_date, end_date, meta):
        if isinstance(start_date, date):
            start_date = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=pytz.UTC)
        if isinstance(end_date, date):
            end_date = datetime.combine(end_date, datetime.min.time()).replace(tzinfo=pytz.UTC)
        grouped_meta = MeasurementConsts.group_meta_by_radius(meta)
        query_set = self.none()
        for radius_in_km, meta_list in grouped_meta.items():
            query_set |= self.filter(measurement_meta__in=meta_list).within_distance(location, radius_in_km)

        query_set = query_set.filter(datetime__range=(start_date, end_date)).filter(measurement_meta__in=meta)
        return query_set.order_by('datetime')

    def within_distance(self, location, max_distance_in_km):
        return self.order_by_distance(location).filter(distance__lt=max_distance_in_km * 1000)

    def order_by_distance(self, location):
        return self.distance(location).order_by('distance')

    def distance(self, location):
        return self.annotate(distance=Distance("location", location))


class MeasurementQuerySet(BaseMeasurementQuerySet):
    def within_hour(self, _datetime, **kwargs):
        """
        :param _datetime: a date time
        :return: all measurements within the hour of the given _datetime.
                e.g. if -datetime is '2022-03-26T22:43:23'
                all measurements between 2022-03-26T22:00:01 and 2022-03-26T23:00:00 are returned.
        """
        previous_hour = _datetime.replace(minute=0, second=1, microsecond=0)
        next_hour = (previous_hour + timedelta(hours=1)).replace(second=0)
        return self.filter(datetime__range=(previous_hour, next_hour), **kwargs)


class Measurement(MeasurementConsts, models.Model):
    datetime = models.DateTimeField()
    location = models.PointField(srid=4326)
    measurement_meta = models.CharField(max_length=20)
    value = models.FloatField()
    data_provider = models.ForeignKey(User, blank=True, null=True, related_name='measurements',
                                      on_delete=models.SET_NULL)

    objects = MeasurementQuerySet.as_manager()

    class Meta:
        ordering = ['datetime', 'location', 'measurement_meta']
        indexes = [
            models.Index(fields=['datetime', 'location'], name='day_location_idx'),
        ]

    def __str__(self):
        return f'{self.datetime} - {self.measurement_meta}'


class HourlyMeasurementQuerySet(BaseMeasurementQuerySet):
    pass


class HourlyMeasurementManager(models.Manager):

    def get_queryset(self):
        return HourlyMeasurementQuerySet(self.model, using=self._db)

    def update_or_create_from_measurement(self, measurement):
        """
         Hourly measurements are calculated from the past hour
         e.g. for 15:00: all measurements from 14:00 up to and including 15:00 are used.

        :param measurement:
        :return: updated or created hourly measurement
        """
        measurements_within_hour = Measurement.objects.within_hour(measurement.datetime,
                                                                   location=measurement.location,
                                                                   measurement_meta=measurement.measurement_meta)
        grouped_value = MeasurementConsts.grouped_value(measurements_within_hour.values_list('value', flat=True),
                                                        measurement.measurement_meta)
        
        hourly_datetime = measurement.datetime.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        self.create(datetime=hourly_datetime, location=measurement.location, value=grouped_value,
                    measurement_meta=measurement.measurement_meta)

    def create(self, **kwargs):
        return super().create(**kwargs)


class HourlyMeasurement(models.Model):
    datetime = models.DateTimeField()
    location = models.PointField(srid=4326)
    measurement_meta = models.CharField(max_length=20)
    value = models.FloatField()

    objects = HourlyMeasurementManager()

    def __str__(self):
        return f'HOURLY: {self.datetime} - {self.measurement_meta}'

