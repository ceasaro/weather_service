from datetime import datetime, timezone

import pydantic

from weather_service.utils.datetime_utils import parse_datetime_in_millis


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
