import datetime
import uuid

from sqlalchemy.orm import Session

from app.database import models
from app.schemas import schemas


def create_room(db: Session, room: schemas.RoomCreate):
    now = datetime.datetime.now()
    db_room = models.Room(
        id=uuid.uuid4(),
        ref_code=uuid.uuid4().hex[:6],
        created_at=now,
        close_at=now + room.duration,
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    db_open_room = models.OpenRoom(id=db_room.id)
    db.add(db_open_room)
    db.commit()
    return db_room


def close_rooms(db: Session):
    now = datetime.datetime.now()
    db_expired_rooms = (
        db.query(models.OpenRoom).filter(models.OpenRoom.room.close_at < now).all()
    )
    for db_expired_room in db_expired_rooms:
        db_closed_room = models.ClosedRoom(id=db_expired_room.id)
        db.add(db_closed_room)
        db.delete(db_expired_room)


def get_room_by_ref_code(db: Session, ref_code: str):
    open_room = (
        db.query(models.OpenRoom)
        .join(models.Room)
        .filter(models.Room.ref_code == ref_code)
        .first()
    )
    if open_room:
        return open_room.room
    else:
        return None


def create_person(db: Session, person: schemas.PersonCreate):
    person = models.Person(**person.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def create_contact(db: Session, contact: schemas.ContactCreate):
    contact = models.Contact(**contact.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
