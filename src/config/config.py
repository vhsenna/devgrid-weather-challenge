import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    OPEN_WEATHER_API_URL = os.getenv("OPEN_WEATHER_API_URL")
