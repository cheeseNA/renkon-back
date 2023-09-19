from fastapi import FastAPI
from app.routers import room

from sqlalchemy.orm import Session

from .database import models
from .database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.include_router(room.router, prefix="/room", tags=["room"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
