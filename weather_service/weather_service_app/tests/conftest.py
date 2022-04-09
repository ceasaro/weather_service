from datetime import timedelta

import pytest
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_datetime

from weather_service.weather_service_app.models import Measurement


@pytest.fixture()
def some_air_temperature_measurements():
    a_date = parse_datetime('2022-03-26T18:43:23+00:00')
    Measurement.objects.bulk_create([
        Measurement(datetime=a_date, location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=13.23),
        Measurement(datetime=a_date + timedelta(hours=1, minutes=2), location=Point(x=6.9, y=52.6, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.701),
        Measurement(datetime=a_date + timedelta(hours=1, minutes=44), location=Point(x=6.7, y=52.9, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.433),
        Measurement(datetime=a_date + timedelta(hours=2, minutes=26), location=Point(x=6.8, y=52.6, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=26.83),
        Measurement(datetime=a_date + timedelta(hours=2, minutes=32), location=Point(x=6.7, y=52.5, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=13.41),
        Measurement(datetime=a_date + timedelta(hours=2, minutes=44), location=Point(x=6.9, y=52.8, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.310),
        Measurement(datetime=a_date + timedelta(hours=3, minutes=52), location=Point(x=6.9, y=52.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=a_date + timedelta(hours=4, minutes=5), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=a_date + timedelta(hours=4, minutes=12), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=a_date + timedelta(hours=4, minutes=33), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=a_date + timedelta(hours=4, minutes=52), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=a_date + timedelta(hours=5, minutes=22), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=a_date + timedelta(hours=5, minutes=41), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=a_date + timedelta(hours=7, minutes=1), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
    ])


@pytest.fixture()
def some_precipitation_measurements():
    a_date = parse_datetime('2022-03-26T18:43:23+00:00')
    Measurement.objects.bulk_create([
        Measurement(datetime=a_date, location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=3.3),
        Measurement(datetime=a_date + timedelta(hours=1, minutes=2), location=Point(x=6.9, y=52.6, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=1.1),
        Measurement(datetime=a_date + timedelta(hours=1, minutes=13), location=Point(x=6.7, y=52.9, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=2.3),
        Measurement(datetime=a_date + timedelta(hours=1, minutes=36), location=Point(x=6.8, y=52.6, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0),
        Measurement(datetime=a_date + timedelta(hours=2, minutes=3), location=Point(x=6.7, y=52.5, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0),
        Measurement(datetime=a_date + timedelta(hours=2, minutes=17), location=Point(x=6.9, y=52.8, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0),
        Measurement(datetime=a_date + timedelta(hours=3, minutes=52), location=Point(x=6.9, y=52.7, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0.2),
    ])


@pytest.fixture()
def some_shortwave_radiation_measurements():
    a_date = parse_datetime('2022-03-26T00:00:00+00:00')
    Measurement.objects.bulk_create([
        Measurement(datetime=a_date, location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=242.2),
        Measurement(datetime=a_date + timedelta(hours=1, minutes=2), location=Point(x=6.9, y=52.6, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=182.1),
        Measurement(datetime=a_date + timedelta(hours=4, minutes=26), location=Point(x=6.8, y=52.6, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=67),
        Measurement(datetime=a_date + timedelta(hours=5, minutes=32), location=Point(x=6.7, y=52.5, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=102),
        Measurement(datetime=a_date + timedelta(hours=6, minutes=52), location=Point(x=6.9, y=52.7, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=21),
        Measurement(datetime=a_date + timedelta(hours=10, minutes=3), location=Point(x=6.9, y=53.1, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=11),
    ])
