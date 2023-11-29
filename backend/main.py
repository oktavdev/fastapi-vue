# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from weather_client import fetch_and_process_weather_data
from models import WeatherResponseData

app = FastAPI()

origins = [
    "http://localhost:8080",  # or the address where your Vue.js app is hosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/weather/", response_model=WeatherResponseData, tags=["weather"])
async def get_weather(latitude: float, longitude: float):
    """
    Get weather data for a given latitude and longitude.
    """
    processed_weather = await fetch_and_process_weather_data(latitude, longitude)
    return processed_weather
