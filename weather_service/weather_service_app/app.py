from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WeatherServiceAppConfig(AppConfig):
    name = 'weather_service.weather_service_app'
    verbose_name = _('weather service app')

    def ready(self):
        import weather_service.weather_service_app.signals
