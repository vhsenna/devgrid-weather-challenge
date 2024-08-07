from src.db.base import Base
from sqlalchemy import JSON, Column, DateTime, String


class WeatherData(Base):
    __tablename__ = "weather_data"

    request_id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime)
    data = Column(JSON)
