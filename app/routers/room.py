from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import crud
from app.database.database import get_db
from app.schemas import schemas

router = APIRouter()


@router.post("/create", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = crud.create_room(db, room)
    return db_room


@router.get("/{ref_code}", response_model=schemas.Room)
def get_room(ref_code: str, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_ref_code(db, ref_code)
    return db_room
