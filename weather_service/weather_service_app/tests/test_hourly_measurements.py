import pytest
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_datetime

from weather_service.weather_service_app.models import HourlyMeasurement, Measurement


@pytest.mark.django_db
def test_create_hourly_measurements():  # some_air_temperature_measurements, some_precipitation_measurements
    m = Measurement(datetime=parse_datetime('2022-03-26T18:43:23+00:00'), location=Point(x=6.8, y=52.7, srid=4326),
                    measurement_meta=Measurement.AIR_TEMPERATURE, value=13.23)
    m.save()
    hourlies = HourlyMeasurement.objects.filter(measurement_meta='AT')
    assert hourlies.count() == 1, \
        "Unexpected amount of hourly measurements"
    assert hourlies[0].datetime == parse_datetime('2022-03-26T19:00:00+00:00')
    assert hourlies[0].value == 13.23
    assert hourlies[0].location == m.location
