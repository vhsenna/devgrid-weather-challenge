import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.models.models import WeatherData
from src.services.services import get_and_save_weather_info, get_weather_info


@pytest.mark.asyncio
async def test_get_weather_info_success():
    city_id = 123456
    expected_response = {
        "main": {
            "temp": 25.0,
            "humidity": 60
        }
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.json = AsyncMock(return_value=expected_response)
        mock_get.return_value.status_code = 200

        result = await get_weather_info(city_id)

        assert result == {
            "city_id": city_id,
            "temperature": 25.0,
            "humidity": 60
        }


@pytest.mark.asyncio
async def test_get_weather_info_http_error():
    city_id = 123456

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=404)
        )

        with pytest.raises(httpx.HTTPStatusError):
            await get_weather_info(city_id)


@pytest.mark.asyncio
async def test_get_and_save_weather_info_success():
    request_id = "test_request_id"
    city_id = 123456
    expected_weather_data = {
        "city_id": city_id,
        "temperature": 25.0,
        "humidity": 60
    }

    with patch("src.services.services.SessionLocal") as mock_session:
        mock_db = mock_session.return_value
        mock_query = mock_db.query.return_value.filter.return_value
        mock_query.first.return_value = None

        with patch("src.services.services.get_weather_info", new_callable=AsyncMock) as mock_get_weather:
            mock_get_weather.return_value = expected_weather_data

            await get_and_save_weather_info(request_id, cities_list=[city_id])

            mock_db.add.assert_called_once()
            args, _ = mock_db.add.call_args
            added_data = args[0]
            assert added_data.request_id == request_id
            assert added_data.data == json.dumps([expected_weather_data])

            mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_and_save_weather_info_update_existing_data():
    request_id = "test_request_id"
    city_id = 123456
    existing_data = [{"city_id": 654321, "temperature": 22.0, "humidity": 55}]
    expected_weather_data = {
        "city_id": city_id,
        "temperature": 25.0,
        "humidity": 60
    }

    with patch("src.services.services.SessionLocal") as mock_session:
        mock_db = mock_session.return_value
        mock_query = mock_db.query.return_value.filter.return_value
        mock_query.first.return_value = WeatherData(
            request_id=request_id,
            timestamp=datetime.now(timezone.utc),
            data=json.dumps(existing_data)
        )

        with patch("src.services.services.get_weather_info", new_callable=AsyncMock) as mock_get_weather:
            mock_get_weather.return_value = expected_weather_data

            await get_and_save_weather_info(request_id, cities_list=[city_id])

            assert len(mock_query.first().data) == 2
            updated_data = json.loads(mock_query.first().data)
            assert updated_data == existing_data + [expected_weather_data]

            mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_and_save_weather_info_closes_db_session():
    request_id = "test_request_id"

    with patch("src.services.services.SessionLocal") as mock_session:
        mock_db = mock_session.return_value

        with patch("src.services.services.get_weather_info", new_callable=AsyncMock) as mock_get_weather:
            mock_get_weather.return_value = {
                "city_id": 123456,
                "temperature": 25.0,
                "humidity": 60
            }

            await get_and_save_weather_info(request_id)

            mock_db.close.assert_called_once()


@pytest.mark.asyncio
async def test_get_and_save_weather_info_handles_exceptions():
    request_id = "test_request_id"
    city_id = 123456

    with patch("src.services.services.SessionLocal") as mock_session:
        mock_db = mock_session.return_value

        with patch("src.services.services.get_weather_info", new_callable=AsyncMock) as mock_get_weather:
            mock_get_weather.side_effect = Exception("Weather data error")

            with pytest.raises(Exception, match="Weather data error"):
                await get_and_save_weather_info(request_id, cities_list=[city_id])

            mock_db.commit.assert_not_called()
