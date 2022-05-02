from datetime import datetime, timezone
from typing import Union

from pydantic.datetime_parse import parse_datetime


def parse_datetime_in_millis(
        value: Union[datetime, str, bytes, int, float]
) -> datetime:
    """
    Parse a datetime/int/float/string in millis and return a datetime.datetime,
    fall back on datetime strings
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, bytes):
        value = value.decode()
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return parse_datetime(value)
    return datetime.fromtimestamp(value / 1000)


def utc_now():
    return datetime.now(tz=timezone.utc)