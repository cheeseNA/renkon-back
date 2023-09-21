from fastapi import FastAPI
from app.routers import room

from app.database import models
from app.database.database import engine
from app.routers import contact, person, room

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(room.router, prefix="/room", tags=["room"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
