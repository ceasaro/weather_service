import pytest
from weather_service.weather_service_app.models import WeatherServiceObject


@pytest.mark.django_db
def test_read_main(api_client):
    data = {"name": "Test weather_service"}
    response = api_client.post("api/v1/weather_service_app/", json=data)
    assert response.status_code == 201
    created_weather_service_object = response.json()
    assert created_weather_service_object["name"] == "Test weather_service"
    assert isinstance(created_weather_service_object["created"], int), "expected created in milli seconds"
    assert WeatherServiceObject.objects.get(uuid=created_weather_service_object["uuid"]).name == "Test weather_service"
    response = api_client.get("api/v1/weather_service_app/")
    assert response.status_code == 200
    weather_service_objects = response.json()
    assert len(weather_service_objects) == 1, "expected one weather_service_object object in response"
