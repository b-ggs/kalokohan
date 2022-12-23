from typing import TypedDict


class Forecast(TypedDict):
    temp_celsius: float
    humidity_percent: int
    feels_like_temp_celsius: float
