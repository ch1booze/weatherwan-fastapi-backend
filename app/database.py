from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

sqlite_url = "sqlite:///db.sqlite"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    from app.models import SQLModel

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
