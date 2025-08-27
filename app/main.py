import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlmodel import select

from app.database import SessionDep, create_db_and_tables
from app.schemas import ModelData, Node, SensorData


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/nodes/", response_model=Node)
def create_node(node: Node, session: SessionDep):
    session.add(node)
    session.commit()
    session.refresh(node)
    return node


@app.get("/nodes/", response_model=list[Node])
def get_nodes(session: SessionDep):
    return session.exec(select(Node)).all()


@app.get("/nodes/{node_id}", response_model=Node)
def get_node(node_id: uuid.UUID, session: SessionDep):
    node = session.get(Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@app.delete("/nodes/{node_id}")
def delete_node(node_id: uuid.UUID, session: SessionDep):
    node = session.get(Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    session.delete(node)
    session.commit()
    return {"detail": "Node deleted"}


@app.get("/nodes/{node_id}/latest-model", response_model=ModelData)
def get_latest_model(node_id: uuid.UUID, session: SessionDep):
    statement = (
        select(ModelData)
        .where(ModelData.node_id == node_id)
        .order_by(ModelData.timestamp.desc())
        .limit(1)
    )
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="No model data found for this node")
    return result


@app.post("/sensor-data/", response_model=SensorData)
def create_sensor_data(data: SensorData, session: SessionDep):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data
