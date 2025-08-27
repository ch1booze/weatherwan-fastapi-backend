import uuid
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class Node(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    created_at: Optional[str] = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    name: str
    location: Optional[str] = None

    sensor_data: List["SensorData"] = Relationship(back_populates="node")
    model_data: List["ModelData"] = Relationship(back_populates="node")


class SensorData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: Optional[str] = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    # Power Consumption Data
    solar_voltage: Optional[float] = None
    solar_current: Optional[float] = None
    battery_voltage: Optional[float] = None
    battery_current: Optional[float] = None
    battery_soc_percent: Optional[float] = None
    ucap_voltage: Optional[float] = None
    ucap_current: Optional[float] = None
    ucap_soc_percent: Optional[float] = None
    load_current: Optional[float] = None

    # Weather Data
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    pressure: Optional[float] = None
    rainfall: Optional[float] = None
    solar_irradiance: Optional[float] = None
    uv_index: Optional[float] = None
    wind_direction: Optional[float] = None

    node_id: uuid.UUID = Field(foreign_key="node.id", nullable=False)
    node: Optional[Node] = Relationship(back_populates="sensor_data")


class ModelData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: Optional[str] = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    data: str
    size: int

    node_id: uuid.UUID = Field(foreign_key="node.id", nullable=False)
    node: Optional[Node] = Relationship(back_populates="model_data")
