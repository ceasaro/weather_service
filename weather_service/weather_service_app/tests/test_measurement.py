import pytest
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_date

from weather_service.weather_service_app.exceptions import WeatherServiceModelException
from weather_service.weather_service_app.models import Measurement, MeasurementConsts


@pytest.mark.django_db
def test_measurement_within_distance(some_air_temperature_measurements):
    km_25 = Measurement.objects.within_distance(location=Point(x=6.8, y=52.7, srid=4326), max_distance_in_km=25)
    assert km_25.count() == 7, "wrong amount of measurements within 25 km"
    km_1 = Measurement.objects.within_distance(location=Point(x=6.8, y=52.7, srid=4326), max_distance_in_km=1)
    assert km_1.count() == 1, "their should be only one measurement within 1 km"
    assert abs(km_1[0].distance.m) < 0.01, "distance should be almost 0"
    assert km_1[0].measurement_meta == 'AT'


@pytest.mark.parametrize("meta_list, grouped_meta, exception", [
    (["AT", "PT", "WD", "RH", "WS"], {10: ["PT"], 20: ["AT", "RH"], 30: ["WD", "WS"], }, None),
    ([], {}, None),
    (["WRONG_META"], {}, WeatherServiceModelException),
])
def test_group_meta_by_radius(meta_list, grouped_meta, exception):
    if exception:
        with pytest.raises(exception):
            MeasurementConsts.group_meta_by_radius(meta_list)
    else:
        assert MeasurementConsts.group_meta_by_radius(meta_list) == grouped_meta


@pytest.mark.django_db
@pytest.mark.parametrize("meta_count", [
    ({'AT': 5}),
    ({'PT': 2}),
    ({'AT': 5, 'PT': 2}),
    ({'AT': 5, 'PT': 2, 'WS': 0, 'RAD_SHORT': 6}),
])
def test_measurement_find(meta_count, some_air_temperature_measurements, some_precipitation_measurements,
                          some_shortwave_radiation_measurements):
    meta_list = meta_count.keys()
    found = Measurement.objects.find(location=Point(x=6.8, y=52.7, srid=4326),
                                     start_date=parse_date('2022-03-26'),
                                     end_date=parse_date('2022-03-27'),
                                     meta=meta_list
                                     )
    total_count = sum(meta_count.values())
    assert found.count() == total_count, f"Expected {total_count} measurements in total"
    for meta, count in meta_count.items():
        meta_measurements = found.filter(measurement_meta=meta)
        assert meta_measurements.count() == count, f"Unexpected amount of {meta} measurements found"
        max_radius_km = MeasurementConsts.DATA.get(meta).get('max_reach_radius_km')
        assert all([m.distance.km <= max_radius_km for m in meta_measurements]), \
            f"All {meta} measurements should be within {max_radius_km}, " \
            f"distances where {[m.distance.km for m in meta_measurements]}"
