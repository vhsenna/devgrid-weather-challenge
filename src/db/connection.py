from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


def init_db():
    Base.metadata.create_all(bind=engine)
