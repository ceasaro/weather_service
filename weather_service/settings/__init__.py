# flake8: noqa
from .base import *

try:
    from .local_settings import *
except ImportError:
    pass

## ##################################################################
## this must be at the bottom of settings.py
## ##################################################################
from django_safe_settings.patch import patch_all
patch_all()