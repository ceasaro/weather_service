from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError

from weather_service.utils import datetime_utils
from weather_service.weather_service_app.models import Measurement, WeatherStation


class Command(BaseCommand):
    help = f"generate a whole lot of measurements in the {settings.DATABASE_PERFORMANCE_TEST} database."

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.weather_station_manager = WeatherStation.objects.using(settings.DATABASE_PERFORMANCE_TEST)
        self.measurement_manager = Measurement.objects.using(settings.DATABASE_PERFORMANCE_TEST)
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument("-i", "--external_id",
                            help="An external field id", )

    def handle(self, external_id=None, **options):

        all_stations = self.weather_station_manager.all()[:3]
        metas = [
            Measurement.AIR_TEMPERATURE,
            Measurement.RELATIVE_HUMIDITY,
            Measurement.PRECIPITATION,
            Measurement.WIND_SPEED,
            Measurement.WIND_DIRECTION
        ]
        _datetime = datetime(year=2020, month=1, day=1).replace(tzinfo=timezone.utc)
        now = datetime_utils.utc_now()
        measurements_per_day = []
        while _datetime < now:
            for hour in range(24):
                for station in all_stations:
                    for meta in metas:
                        measurements_per_day.append(
                            Measurement(datetime=_datetime, location=station.location,
                                        measurement_meta=meta, value=1.1,
                                        station=station, ))
                _datetime = _datetime + timedelta(hours=1)
            if len(measurements_per_day) > 10000:
                self.create_bulk_measurements(measurements_per_day)
                measurements_per_day = []
        if len(measurements_per_day) > 0:
            self.create_bulk_measurements(measurements_per_day)

    def create_bulk_measurements(self, measurements_per_day):
        try:
            self.measurement_manager.bulk_create(measurements_per_day)
            print(f"stored {len(measurements_per_day)} measurements.")
        except IntegrityError:
            print(f"Error storing measurements because some of the measurements in bulk already exist in the db.")
