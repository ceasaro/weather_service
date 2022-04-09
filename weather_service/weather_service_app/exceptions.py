class WeatherServiceException(Exception):
    pass


class WeatherServiceModelException(WeatherServiceException):
    """Some exception in the weather model occurred"""
    pass
