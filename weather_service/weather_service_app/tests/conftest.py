from datetime import timedelta

import pytest
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_datetime

from weather_service.weather_service_app.models import Measurement


@pytest.fixture()
def some_air_temperature_measurements():
    a_date = parse_datetime('2022-03-26T18:43:23')
    Measurement.objects.bulk_create([
        Measurement(day=a_date, location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=13.23),
        Measurement(day=a_date + timedelta(hours=1, minutes=2), location=Point(x=6.9, y=52.6, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.701),
        Measurement(day=a_date + timedelta(hours=2, minutes=44), location=Point(x=6.7, y=52.9, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.433),
        Measurement(day=a_date + timedelta(hours=4, minutes=26), location=Point(x=6.8, y=52.6, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=26.83),
        Measurement(day=a_date + timedelta(hours=5, minutes=32), location=Point(x=6.7, y=52.5, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=13.41),
        Measurement(day=a_date + timedelta(hours=6, minutes=4), location=Point(x=6.9, y=52.8, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.310),
        Measurement(day=a_date + timedelta(hours=6, minutes=52), location=Point(x=6.9, y=52.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
    ])
