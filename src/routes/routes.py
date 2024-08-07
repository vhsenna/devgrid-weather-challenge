import json

from fastapi import APIRouter, HTTPException

from src.db.connection import SessionLocal
from src.models.models import WeatherData
from src.schemas.schemas import (
    UserWeatherRequest,
    WeatherDataResponse,
    WeatherProgressResponse,
)
from src.services.services import get_and_save_weather_info
from src.utils.cities import CITIES_ID

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to the DevGrid Weather Challenge"}


@router.post("/weather/", response_model=WeatherDataResponse)
async def start_weather_data_collection(request: UserWeatherRequest):
    try:
        with SessionLocal() as db:
            existing_user_record = db.query(WeatherData).filter(
                WeatherData.request_id == request.request_id).first()

            if existing_user_record:
                raise HTTPException(
                    status_code=400, detail="User ID already exists in the system.")

            await get_and_save_weather_info(request.request_id)

        return {"message": "Weather data collection has been successfully initiated."}

    except HTTPException as e:
        print(f"HTTPException occurred: {e.detail}")
        raise

    except Exception as general_exception:
        print(f"An unexpected error occurred: {general_exception}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred. Please try again later.")


@router.get("/weather/{request_id}", response_model=WeatherProgressResponse)
async def get_weather_data(request_id: str):
    if not request_id.strip():
        raise HTTPException(
            status_code=422, detail="Request ID cannot be empty.")

    total_cities = len(CITIES_ID)

    try:
        with SessionLocal() as db:
            weather_record = db.query(WeatherData).filter(
                WeatherData.request_id == request_id).first()

            if not weather_record:
                raise HTTPException(
                    status_code=404, detail="User ID cannot be found in the database.")

            entries_count = len(json.loads(weather_record.data))

            upload_progress = int((entries_count / total_cities) * 100)

            result_data = {
                "request_id": weather_record.request_id,
                "timestamp": weather_record.timestamp,
                "data": weather_record.data,
                "upload_progress": f"{upload_progress}% uploaded..."
            }

            return result_data

    except HTTPException as e:
        print(f"HTTPException occurred: {e.detail}")
        raise

    except Exception as general_exception:
        print(f"An unexpected error occurred: {general_exception}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred. Please try again later.")
