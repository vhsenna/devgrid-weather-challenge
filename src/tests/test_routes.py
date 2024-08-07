
import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.models.models import WeatherData
from src.schemas.schemas import UserWeatherRequest

client = TestClient(app)


@pytest.fixture
def mock_db_session():
    with patch("src.routes.routes.SessionLocal") as mock_session:
        yield mock_session.return_value


@pytest.mark.asyncio
async def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the DevGrid Weather Challenge"}


@pytest.mark.asyncio
async def test_start_weather_data_collection_success():
    request_data = UserWeatherRequest(request_id="unique_request_id")

    with patch("src.routes.routes.get_and_save_weather_info", new_callable=AsyncMock) as mock_get_and_save:
        mock_get_and_save.return_value = None
        response = client.post("/weather/", json=request_data.model_dump())
        assert response.status_code == 200
        assert response.json() == {
            "message": "Weather data collection has been successfully initiated."}


@pytest.mark.asyncio
async def test_start_weather_data_collection_user_id_exists():
    request_data = UserWeatherRequest(request_id="existing_request_id")

    with patch("src.routes.routes.SessionLocal") as mock_session:
        mock_db = mock_session.return_value
        mock_db.query.return_value.filter.return_value.first.return_value = WeatherData(
            request_id="existing_request_id")

        response = client.post("/weather/", json=request_data.dict())
        assert response.status_code == 400
        assert response.json() == {
            "detail": "User ID already exists in the system."}


@pytest.mark.asyncio
async def test_start_weather_data_collection_exception():
    request_data = UserWeatherRequest(request_id="unique_request_id")

    with patch("src.routes.routes.get_and_save_weather_info", new_callable=AsyncMock) as mock_get_and_save:
        mock_get_and_save.side_effect = Exception("General error")
        response = client.post("/weather/", json=request_data.dict())
        assert response.status_code == 500
        assert response.json() == {
            "detail": "An unexpected error occurred. Please try again later."}


@pytest.mark.asyncio
async def test_get_weather_data_success():
    request_id = "valid_request_id"
    mock_weather_data = WeatherData(request_id=request_id, timestamp="2024-01-01T00:00:00Z",
                                    data=json.dumps([{"city_id": 3439525, "temperature": 20.0, "humidity": 70}]))

    with patch("src.routes.routes.SessionLocal") as mock_session:
        mock_db = mock_session.return_value
        mock_db.query.return_value.filter.return_value.first.return_value = mock_weather_data

        response = client.get(f"/weather/{request_id}")
        assert response.status_code == 200
        assert response.json() == {
            "request_id": request_id,
            "timestamp": "2024-01-01T00:00:00Z",
            "data": json.dumps([{"city_id": 3439525, "temperature": 20.0, "humidity": 70}]),
            "upload_progress": "100% uploaded..."
        }


@pytest.mark.asyncio
async def test_get_weather_data_request_id_empty():
    response = client.get("/weather/")
    assert response.status_code == 422
    assert response.json() == {"detail": "Request ID cannot be empty."}


@pytest.mark.asyncio
async def test_get_weather_data_request_id_not_found():
    request_id = "nonexistent_request_id"

    with patch("src.routes.routes.SessionLocal") as mock_session:
        mock_db = mock_session.return_value
        mock_db.query.return_value.filter.return_value.first.return_value = None

        response = client.get(f"/weather/{request_id}")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "User ID cannot be found in the database."}


@pytest.mark.asyncio
async def test_get_weather_data_exception():
    request_id = "valid_request_id"

    with patch("src.routes.routes.SessionLocal") as mock_session:
        mock_db = mock_session.return_value
        mock_db.query.return_value.filter.return_value.first.side_effect = Exception(
            "General error")

        response = client.get(f"/weather/{request_id}")
        assert response.status_code == 500
        assert response.json() == {
            "detail": "An unexpected error occurred. Please try again later."}
