from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class SensorData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(index=True)
    temperature: Mapped[float]
    humidity: Mapped[float]
    pressure: Mapped[float]

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
        }
