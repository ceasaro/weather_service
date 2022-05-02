from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand

from weather_service.performance.weather_station_data import WEATHER_STATION_LOCATIONS
from weather_service.weather_service_app.models import Measurement, WeatherStation


class Command(BaseCommand):
    help = f"performance test fetching measurements from the {settings.DATABASE_PERFORMANCE_TEST} database"

    def handle(self, **options):
        measurement_manager = Measurement.objects.using(settings.DATABASE_PERFORMANCE_TEST)
        print(measurement_manager.all().count())

