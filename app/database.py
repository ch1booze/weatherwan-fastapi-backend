import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class SensorData(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().hex)
    device_id: Mapped[str] = mapped_column(index=True)
    temperature: Mapped[float]
    humidity: Mapped[float]
    pressure: Mapped[float]
