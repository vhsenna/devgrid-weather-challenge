from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class UserWeatherRequest(BaseModel):
    request_id: str = Field(..., description="ID provided by the user.")

    @field_validator("request_id")
    def request_id_is_valid(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Request ID cannot be blank.")
        return value


class WeatherDataResponse(BaseModel):
    message: str


class UserWeatherData(BaseModel):
    request_id: str
    timestamp: datetime
    data: list[dict[str, Any]]

    class Config():
        from_attributes = True


class WeatherProgressResponse(BaseModel):
    request_id: str
    timestamp: datetime
    data: str
    upload_progress: str
