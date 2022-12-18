import datetime

from django.conf import settings
from django.utils.module_loading import import_string
from faker import Faker
from pydantic.utils import import_string

from .types import Forecast

fake = Faker()


class BaseOpenMeteoClient:
    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url

    def get_hourly_forecast(
        self,
        latitude: float,
        longitude: float,
        date: datetime.date,
    ) -> dict[str, Forecast]:
        """
        Returns the hourly temperature, relative humidity, and apparent
        temperature for a location on the date (UTC) specified.

        Returns a dictionary whose key is the datetime in the format
        %Y-%m-%dT%H:00 and the value a dictionary defined by the attributes in
        Forecast.

        ex.
        {
            "2022-12-04T00:00": {
                "temp_celsius": 27.5,
                "relat_humidity_percent": 82,
                "feels_like_temp_celsius": 32.4
            },
            ...
        }
        """
        raise NotImplementedError()


class DummyOpenMeteoClient(BaseOpenMeteoClient):
    def get_hourly_forecast(
        self,
        latitude: float,
        longitude: float,
        date: datetime.date,
    ) -> dict[str, Forecast]:
        """
        Returns the hourly temperature, relative humidity, and apparent
        temperature for a location on the date (UTC) specified.

        Returns a dictionary whose key is the datetime in the format
        %Y-%m-%dT%H:00 and the value a dictionary defined by the attributes in
        Forecast.

        ex.
        {
            "2022-12-04T00:00": {
                "temp_celsius": 27.5,
                "humidity_percent": 82,
                "feels_like_temp_celsius": 32.4
            },
            ...
        }
        """
        resp: dict[str, Forecast] = {}

        for hour in range(0, 24):
            hour_padded = str(hour).ljust(2, "0")
            key = date.strftime("%Y-%m-%dT") + f"{hour_padded}:00"

            temp_celsius: float = fake.pyfloat(
                right_digits=1,
                min_value=20.0,
                max_value=35.0,
            )

            humidity_percent: int = fake.pyint(
                min_value=50,
                max_value=90,
            )

            feels_like_temp_celsius: float = fake.pyfloat(
                right_digits=1,
                min_value=20.0,
                max_value=35.0,
            )

            resp[key] = Forecast(
                temp_celsius=temp_celsius,
                humidity_percent=humidity_percent,
                feels_like_temp_celsius=feels_like_temp_celsius,
            )

        return resp


def get_open_meteo_client(**kwargs) -> BaseOpenMeteoClient:
    client_class = import_string(settings.WEATHER_OPEN_METEO_CLIENT_CLASS)
    return client_class(**kwargs)
