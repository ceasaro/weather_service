from django.db.models.signals import post_save
from django.dispatch import receiver

from weather_service.weather_service_app.models import Measurement, HourlyMeasurement


@receiver(post_save, sender=Measurement)
def update_hourly_measurement(sender, instance: Measurement, **kwargs):
    HourlyMeasurement.objects.update_or_create_from_measurement(instance)
    print(f"Updating hourly with: {instance}")
