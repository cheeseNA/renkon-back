from fastapi import FastAPI

from app.database import models
from app.database.database import engine
from app.routers import contact, person, room

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(room.router, prefix="/room", tags=["room"])
app.include_router(person.router, prefix="/person", tags=["person"])
app.include_router(contact.router, prefix="/contact", tags=["contact"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
