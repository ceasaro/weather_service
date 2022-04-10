from datetime import timedelta

import pytest
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_datetime

from weather_service.weather_service_app.models import Measurement


@pytest.fixture()
def some_air_temperature_measurements():
    Measurement.objects.bulk_create([
        Measurement(datetime=parse_datetime('2022-03-26 18:43:23+00:00'), location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=13.23),
        Measurement(datetime=parse_datetime('2022-03-26 19:44:23+00:00'), location=Point(x=6.9, y=52.6, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.701),
        Measurement(datetime=parse_datetime('2022-03-26 20:27:23+00:00'), location=Point(x=6.7, y=52.9, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.433),
        Measurement(datetime=parse_datetime('2022-03-26 21:09:23+00:00'), location=Point(x=6.8, y=52.6, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=26.83),
        Measurement(datetime=parse_datetime('2022-03-26 21:15:23+00:00'), location=Point(x=6.7, y=52.5, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=13.41),
        Measurement(datetime=parse_datetime('2022-03-26 22:00:00+00:00'), location=Point(x=6.9, y=52.8, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.310),
        Measurement(datetime=parse_datetime('2022-03-26 22:00:01+00:00'), location=Point(x=6.9, y=52.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-26 22:13:24+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-26 22:25:23+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-26 22:46:23+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-26 23:00:00+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-26 23:43:23+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-27 00:05:23+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-27 00:24:23+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
        Measurement(datetime=parse_datetime('2022-03-27 01:44:23+00:00'), location=Point(x=7.8, y=53.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=0.6),
    ])


@pytest.fixture()
def some_precipitation_measurements():
    Measurement.objects.bulk_create([
        Measurement(datetime=parse_datetime('2022-03-26 18:43:23+00:00'), location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=3.3),
        Measurement(datetime=parse_datetime('2022-03-26 20:44:23+00:00'), location=Point(x=6.9, y=52.6, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=1.1),
        Measurement(datetime=parse_datetime('2022-03-26 20:27:23+00:00'), location=Point(x=6.7, y=52.9, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=2.3),
        Measurement(datetime=parse_datetime('2022-03-26 21:09:23+00:00'), location=Point(x=6.8, y=52.6, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0),
        Measurement(datetime=parse_datetime('2022-03-26 21:15:23+00:00'), location=Point(x=6.7, y=52.5, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0),
        Measurement(datetime=parse_datetime('2022-03-26 21:27:23+00:00'), location=Point(x=6.9, y=52.8, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0),
        Measurement(datetime=parse_datetime('2022-03-26 22:00:01+00:00'), location=Point(x=6.9, y=52.7, srid=4326),
                    measurement_meta=Measurement.PRECIPITATION, value=0.2),
    ])


@pytest.fixture()
def some_shortwave_radiation_measurements():
    a_date = parse_datetime('2022-03-26T00:00:00+00:00')
    Measurement.objects.bulk_create([
        Measurement(datetime=parse_datetime('2022-03-26 00:00:00+00:00'), location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=242.2),
        Measurement(datetime=parse_datetime('2022-03-26 01:02:00+00:00'), location=Point(x=6.9, y=52.6, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=182.1),
        Measurement(datetime=parse_datetime('2022-03-26 04:26:00+00:00'), location=Point(x=6.8, y=52.6, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=67),
        Measurement(datetime=parse_datetime('2022-03-26 05:32:00+00:00'), location=Point(x=6.7, y=52.5, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=102),
        Measurement(datetime=parse_datetime('2022-03-26 06:52:00+00:00'), location=Point(x=6.9, y=52.7, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=21),
        Measurement(datetime=parse_datetime('2022-03-26 10:03:00+00:00'), location=Point(x=6.9, y=53.1, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=11),
        Measurement(datetime=parse_datetime('2022-03-26 22:03:00+00:00'), location=Point(x=6.9, y=54.1, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=21),
        Measurement(datetime=parse_datetime('2022-03-26 22:53:00+00:00'), location=Point(x=7.3, y=54.2, srid=4326),
                    measurement_meta=Measurement.RADIATION_SHORTWAVE, value=14),
    ])
