import httpx
from fastapi import HTTPException

from models import WeatherResponseData

async def fetch_and_process_weather_data(latitude: float, longitude: float) -> WeatherResponseData:
    """
    Fetch and process weather data from an external API.
    """
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
        else:
            raise HTTPException(status_code=response.status_code, detail="Weather API request failed")

    return process_weather_data(weather_data)

def process_weather_data(weather_data) -> WeatherResponseData:
    """
    Process the weather data.
    """
    k = ['time', 'temperature_2m_min', 'temperature_2m_max', 'precipitation_probability_max', 'wind_speed_10m_max']
    a = weather_data['daily']['time']
    b = weather_data['daily']['temperature_2m_min']
    c = weather_data['daily']['temperature_2m_max']
    d = weather_data['daily']['precipitation_probability_max']
    e = weather_data['daily']['wind_speed_10m_max']
    weather = [dict(zip(k, values)) for values in list(zip(a, b, c, d, e))]

    weather_response = WeatherResponseData(
        weather=weather,
        daily_units=weather_data['daily_units']
    )

    return weather_response