from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import crud
from app.database.database import get_db
from app.schemas import schemas

router = APIRouter()


@router.post("/create", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.create_person(db, person)
    return db_person
