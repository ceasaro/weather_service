from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand

from weather_service.performance.weather_station_data import WEATHER_STATION_LOCATIONS
from weather_service.weather_service_app.models import WeatherStation


class Command(BaseCommand):
    help = f"creates weather stations in the {settings.DATABASE_PERFORMANCE_TEST} database."

    def handle(self, **options):
        for station in WEATHER_STATION_LOCATIONS:
            name = station.get('name')
            location = Point.from_ewkt(station.get('geo_json'))
            # print(WeatherStation.objects.all().using(settings.DATABASE_PERFORMANCE_TEST))
            WeatherStation.objects \
                .using(settings.DATABASE_PERFORMANCE_TEST) \
                .update_or_create(location=location, defaults={'name': name})
