import pytest
from sqlalchemy import JSON, DateTime, String, create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.models.models import WeatherData

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_table_creation(setup_database):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "weather_data" in tables, "Table 'weather_data' should be created."


def test_column_types(setup_database):
    inspector = inspect(engine)
    columns = inspector.get_columns("weather_data")

    column_types = {col["name"]: col["type"] for col in columns}

    assert isinstance(
        column_types["request_id"], String), "Column 'request_id' should be of type String."
    assert isinstance(
        column_types["timestamp"], DateTime), "Column 'timestamp' should be of type DateTime."
    assert isinstance(column_types["data"],
                      JSON), "Column 'data' should be of type JSON."


def test_column_existence(setup_database):
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns("weather_data")]

    assert "request_id" in columns, "Column 'request_id' should exist."
    assert "timestamp" in columns, "Column 'timestamp' should exist."
    assert "data" in columns, "Column 'data' should exist."
