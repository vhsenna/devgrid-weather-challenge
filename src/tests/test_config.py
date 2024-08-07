import os

import pytest
from dotenv import load_dotenv

from src.config.config import Config

load_dotenv()


@pytest.fixture(scope="module", autouse=True)
def setup_env():
    os.environ["OPEN_WEATHER_API_KEY"] = "test_api_key"
    yield
    del os.environ["OPEN_WEATHER_API_KEY"]


def test_open_weather_api_key():
    assert Config.OPEN_WEATHER_API_KEY == Config.OPEN_WEATHER_API_KEY, "OPEN_WEATHER_API_KEY should be 'test_api_key'"
