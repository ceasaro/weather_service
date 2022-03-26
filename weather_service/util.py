from datetime import datetime, timezone
from typing import Union

import pydantic
from pydantic.datetime_parse import parse_datetime

import uuid
from django.db import models


def snake2camel(snake: str) -> str:
    """
    Converts a snake_case string to camelCase.
    """
    camel = snake.title()
    return camel[0].lower() + camel[1:].replace("_", "")


class DateTimeInMillis(int):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime_in_millis
        yield cls.ensure_tzinfo

    @classmethod
    def ensure_tzinfo(cls, v):
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)

    @staticmethod
    def to_str(dt: datetime) -> str:
        return f"{(dt.timestamp() * 1000):.0f}"

    @staticmethod
    def to_int(dt: datetime) -> int:
        return int(dt.timestamp() * 1000)


class APIModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake2camel
        json_encoders = {datetime: DateTimeInMillis.to_int}


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


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True
