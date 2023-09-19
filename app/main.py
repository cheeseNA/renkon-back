from fastapi import FastAPI
from app.routers import room


app = FastAPI()

app.include_router(room.router, prefix="/room", tags=["room"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
