from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.schemas import (
    UserWeatherData,
    UserWeatherRequest,
    WeatherDataResponse,
    WeatherProgressResponse,
)


def test_user_weather_request_valid():
    request = UserWeatherRequest(request_id="valid_id")
    assert request.request_id == "valid_id"


def test_user_weather_request_blank_id():
    with pytest.raises(ValidationError):
        UserWeatherRequest(request_id="")


def test_weather_data_response():
    response = WeatherDataResponse(message="Data collection initiated.")
    assert response.message == "Data collection initiated."


def test_user_weather_data():
    data = UserWeatherData(
        request_id="test_id",
        timestamp=datetime(2024, 8, 6, 12, 0, 0),
        data=[{"city_id": 3439525, "temperature": 25, "humidity": 80}]
    )
    assert data.request_id == "test_id"
    assert data.timestamp == datetime(2024, 8, 6, 12, 0, 0)
    assert data.data == [
        {"city_id": 3439525, "temperature": 25, "humidity": 80}]


def test_weather_progress_response():
    response = WeatherProgressResponse(
        request_id="test_id",
        timestamp=datetime(2024, 8, 6, 12, 0, 0),
        data='{"city_id": 3439525, "temperature": 25, "humidity": 80"}',
        upload_progress="50% uploaded..."
    )
    assert response.request_id == "test_id"
    assert response.timestamp == datetime(2024, 8, 6, 12, 0, 0)
    assert response.data == '{"city_id": 3439525, "temperature": 25, "humidity": 80"}'
    assert response.upload_progress == "50% uploaded..."


def test_user_weather_data_invalid_data():
    with pytest.raises(ValueError):
        UserWeatherData(
            request_id="test_id",
            timestamp=datetime(2024, 8, 6, 12, 0, 0),
            data="Invalid data format"
        )


if __name__ == "__main__":
    pytest.main()
