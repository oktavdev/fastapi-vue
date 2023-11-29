from typing import Union, List

from pydantic import BaseModel


class Weather(BaseModel):
    time: str
    temperature_2m_max: Union[None, float]
    temperature_2m_min: Union[None, float]
    precipitation_probability_max: Union[None, float]
    wind_speed_10m_max: Union[None, float]


class WeatherResponseData(BaseModel):
    daily_units: dict
    weather: List[Weather]
