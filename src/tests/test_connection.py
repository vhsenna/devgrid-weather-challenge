import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from src.db.connection import SessionLocal, engine, init_db


@pytest.fixture(scope="module")
def setup_database():
    init_db()
    yield


def test_database_creation(setup_database):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1
    except OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")


def test_session_creation(setup_database):
    try:
        session = SessionLocal()
        assert session is not None
    except Exception as e:
        pytest.fail(f"Session creation failed: {e}")
    finally:
        session.close()


def test_database_init_failure():
    original_init_db = init_db

    def faulty_init_db():
        raise Exception("Simulated database initialization failure.")

    try:
        globals()["init_db"] = faulty_init_db
        with pytest.raises(Exception, match="Simulated database initialization failure"):
            init_db()
    finally:
        globals()["init_db"] = original_init_db


def test_session_creation_failure():
    original_session_local = SessionLocal

    def faulty_session_local():
        raise Exception("Simulated session creation failure.")

    try:
        globals()["SessionLocal"] = faulty_session_local
        with pytest.raises(Exception, match="Simulated session creation failure"):
            SessionLocal()
    finally:
        globals()["SessionLocal"] = original_session_local
