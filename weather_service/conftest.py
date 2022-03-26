import pytest
from fastapi.testclient import TestClient

from weather_service.asgi import application


@pytest.fixture
def api_client():
    return TestClient(application)
