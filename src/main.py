from fastapi import FastAPI

from src.db.connection import init_db
from src.routes.routes import router as weather_router

init_db()

app = FastAPI()

app.include_router(weather_router)
