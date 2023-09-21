from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import crud
from app.database.database import get_db
from app.schemas import schemas

router = APIRouter()


@router.post("/create", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.create_contact(db, contact)
    return db_contact
