import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "TODO_REPLACE_django-insecure-r1&pqt40#t1xh$$h@=bjp2-0veuu9*tl!--vaa+zdm5br#f+1+",
)

DEBUG = False
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_safe_settings",
    "django_extensions",
    # Our apps
    "weather_service.weather_service_app.app.WeatherServiceAppConfig",
    "weather_service.performance",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "weather_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "weather_service.wsgi.application"
DATABASE_PERFORMANCE_TEST = "performance"
DATABASES = {
    "default": {
    },
    DATABASE_PERFORMANCE_TEST: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'weather_service_performance',
        'USER': 'cees',
        'PASSWORD': 'welkom',
        'HOST': '127.0.0.1',
        'PORT': '5438',
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WSGI_APP_URL = "/web"
API_V1_URL = "/api/v1"
PROJECT_NAME = "weather_service"
STATIC_ROOT = "static"

# Example secret. Make sure it starts with SECRET_, so django wil scrub them even in debug mode.
# Use `./manage.py django_safe_settings_encrypt PLAIN_DATA` to get the encrypted value
# https://pypi.org/project/django-safe-settings/
SECRET_TESTSECRET = "enc:91cae7433e46684ac16a302f39b756b3"
