import pytest
from django.contrib.gis.geos import Point

from weather_service.weather_service_app.models import Measurement


@pytest.mark.django_db
def test_measurement_within_distance(some_air_temperature_measurements):
    km_25 = Measurement.objects.within_distance(location=Point(x=6.8, y=52.7, srid=4326), max_distance_in_km=25)
    assert km_25.count() == 7, "wrong amount of measurements within 25 km"
    km_1 = Measurement.objects.within_distance(location=Point(x=6.8, y=52.7, srid=4326), max_distance_in_km=1)
    assert km_1.count() == 1, "their should be only one measurement within 1 km"
    assert abs(km_1[0].distance.m) < 0.01, "distance should be almost 0"
    assert km_1[0].measurement_meta == 'AT'

