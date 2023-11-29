# main.py
from typing import Union, List

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:8080",  # or the address where your Vue.js app is hosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Weather(BaseModel):
    time: str
    temperature_2m_max: Union[None, float]
    temperature_2m_min: Union[None, float]
    precipitation_probability_max: Union[None, float]
    wind_speed_10m_max: Union[None, float]

class WeatherResponseData(BaseModel):
    daily_units: dict
    weather: List[Weather]


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/weather/", response_model=WeatherResponseData, tags=["weather"])
async def get_weather(latitude: float, longitude: float):

    """
    TODO: Add docstring
    """

    # A free weather data API provider for showcasing
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset",
                  "precipitation_probability_max", "wind_speed_10m_max"],
        "forecast_days": 16
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        if response.status_code == 200:

            weather_data = response.json()

            # Process the data zip keys and values TODO: Move to separate method
            k = ['time', 'temperature_2m_min', 'temperature_2m_max', 'precipitation_probability_max', 'wind_speed_10m_max']
            a = weather_data['daily']['time']
            b = weather_data['daily']['temperature_2m_min']
            c = weather_data['daily']['temperature_2m_max']
            d = weather_data['daily']['precipitation_probability_max']
            e = weather_data['daily']['wind_speed_10m_max']
            weather = [dict(zip(k, values)) for values in list(zip(a, b, c, d, e))]

            weather_response = {
                'weather': weather,
                'daily_units': weather_data['daily_units']
            }

            return weather_response
        else:
            raise HTTPException(status_code=response.status_code, detail="Weather API request failed")