import pytest
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_datetime

from weather_service.weather_service_app.models import HourlyMeasurement, Measurement


@pytest.mark.django_db
def test_create_hourly_measurements_air_temperature():
    Measurement.objects.create(datetime=parse_datetime('2022-03-26T18:43:23+00:00'),
                               location=Point(x=6.8, y=52.7, srid=4326),
                               measurement_meta=Measurement.AIR_TEMPERATURE, value=12.0)
    hourlies = HourlyMeasurement.objects.filter(measurement_meta='AT')
    assert hourlies.count() == 1, "Only expected 1 hourly measurement"
    assert hourlies[0].datetime == parse_datetime('2022-03-26T18:00:00+00:00')
    assert hourlies[0].value == 12.0

    Measurement.objects.create(datetime=parse_datetime('2022-03-26T18:59:59+00:00'),
                               location=Point(x=6.8, y=52.7, srid=4326),
                               measurement_meta=Measurement.AIR_TEMPERATURE, value=14.0)
    hourlies = HourlyMeasurement.objects.filter(measurement_meta='AT')
    assert hourlies.count() == 1, "Only expected 1 hourly measurement, cause all measurements are within the hour"
    assert hourlies[0].datetime == parse_datetime('2022-03-26T18:00:00+00:00')
    assert hourlies[0].value == 13.0

    Measurement.objects.create(datetime=parse_datetime('2022-03-26T18:00:00+00:00'),
                               location=Point(x=6.8, y=52.7, srid=4326),
                               measurement_meta=Measurement.AIR_TEMPERATURE, value=16.0)
    hourlies = HourlyMeasurement.objects.filter(measurement_meta='AT')
    assert hourlies.count() == 1, "Only expected 1 hourly measurement, cause all measurements are within the hour"
    assert hourlies[0].datetime == parse_datetime('2022-03-26T18:00:00+00:00')
    assert hourlies[0].value == 14.0

    Measurement.objects.create(datetime=parse_datetime('2022-03-26T19:00:00+00:00'),
                               location=Point(x=6.8, y=52.7, srid=4326),
                               measurement_meta=Measurement.AIR_TEMPERATURE, value=17.0)
    hourlies = HourlyMeasurement.objects.filter(measurement_meta='AT')
    assert hourlies.count() == 2, "expected 2 hourly measurement, cause not all measurements are within an hour"
    assert hourlies[0].datetime == parse_datetime('2022-03-26T18:00:00+00:00')
    assert hourlies[0].value == 14.0
    assert hourlies[1].datetime == parse_datetime('2022-03-26T19:00:00+00:00')
    assert hourlies[1].value == 17.0
