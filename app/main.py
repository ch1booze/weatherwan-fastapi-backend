from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import select

from app.database import SessionDep, create_db_and_tables
from app.models import ModelData, WeatherData


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    await app.state.db.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/weather-data")
async def add_weather_data(weather_data: WeatherData, session: SessionDep):
    session.add(weather_data)
    session.commit()
    session.refresh(weather_data)
    return weather_data


@app.get("/model-data")
async def get_model_data(session: SessionDep):
    statement = select(ModelData)
    model_data = session.exec(statement).first()
    return model_data
