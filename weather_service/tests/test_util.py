import pytest

from weather_service.utils.util import snake2camel


@pytest.mark.parametrize('snake_str, camel_str', [
    ('foo', 'foo'),
    ('foo_bar', 'fooBar'),
])
def test_snake2camel(snake_str, camel_str):
    assert snake2camel(snake_str) == camel_str
