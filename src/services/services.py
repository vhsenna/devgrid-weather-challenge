import json
from datetime import datetime, timezone
from typing import Any

import httpx

from src.config.config import Config
from src.db.connection import SessionLocal
from src.models.models import WeatherData
from src.utils.cities import CITIES_ID


async def get_weather_info(city_id: int) -> dict[str, Any]:
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        weather_response = await client.get(
            Config.OPEN_WEATHER_API_URL,
            params={
                "id": city_id,
                "appid": Config.OPEN_WEATHER_API_KEY,
                "units": "metric",
            }
        )
        weather_response.raise_for_status()
        weather_json = weather_response.json()
        return {
            "city_id": city_id,
            "temperature": weather_json["main"]["temp"],
            "humidity": weather_json["main"]["humidity"],
        }


async def get_and_save_weather_info(request_id: str, cities_list: list = CITIES_ID) -> None:
    database_session = SessionLocal()
    try:
        for city in cities_list:
            city_weather = await get_weather_info(city)

            record = database_session.query(WeatherData).filter(
                WeatherData.request_id == request_id
            ).first()

            if record is not None:
                current_data = json.loads(record.data) if record.data else []
                current_data.append(city_weather)
                record.data = json.dumps(current_data)
            else:
                new_weather_data = WeatherData(
                    request_id=request_id,
                    timestamp=datetime.now(timezone.utc),
                    data=json.dumps([city_weather])
                )
                database_session.add(new_weather_data)

            database_session.commit()
            database_session.refresh(record if record else new_weather_data)
    finally:
        database_session.close()
