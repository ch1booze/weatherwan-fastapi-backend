import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Telemetry(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().hex)
    node: Mapped[str] = mapped_column(index=True)
    data: Mapped[str]
