import os

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_service.settings")
apps.populate(settings.INSTALLED_APPS)

from weather_service.api_router import router as api_router  # noqa: E402

wsgi_application = get_wsgi_application()


def get_application() -> FastAPI:
    _application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_URL}/openapi.json",
        debug=settings.DEBUG,
    )

    _application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_HOSTS] or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _application.include_router(api_router, prefix=settings.API_V1_URL)
    _application.mount(
        f"{settings.WSGI_APP_URL}/static",
        StaticFiles(directory="static"),
        name="static",
    )
    _application.mount(f"{settings.WSGI_APP_URL}", WSGIMiddleware(wsgi_application))
    return _application


application = get_application()
