from sqlmodel import Column, DateTime, Field, Float, SQLModel, String, func


class WeatherData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    node: str = Field(sa_column=Column(String(80), nullable=False))
    temperature: float = Field(sa_column=Column(Float, nullable=False))
    humidity: float = Field(sa_column=Column(Float, nullable=False))
    wind_speed: float = Field(sa_column=Column(Float, nullable=False))
    precipitation: float = Field(sa_column=Column(Float, nullable=False))
    atmospheric_pressure: float = Field(sa_column=Column(Float, nullable=False))
    uv_index: float = Field(sa_column=Column(Float, nullable=False))
    visibility: float = Field(sa_column=Column(Float, nullable=False))
    timestamp: str | None = Field(sa_column=Column(DateTime, server_default=func.now()))
