import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from .database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Uuid, primary_key=True, index=True)
    ref_code = Column(String(6), index=True)
    created_at = Column(DateTime)
    close_at = Column(DateTime)

    persons = relationship("Person", back_populates="room")


class OpenRoom(Base):
    __tablename__ = "open_rooms"

    id = Column(Uuid, ForeignKey("rooms.id"), primary_key=True, index=True)

    room = relationship("Room")


class ClosedRoom(Base):
    __tablename__ = "closed_rooms"

    id = Column(Uuid, ForeignKey("rooms.id"), primary_key=True, index=True)

    room = relationship("Room")


class Person(Base):
    __tablename__ = "persons"

    id = Column(Uuid, primary_key=True, index=True)
    name = Column(String(32), index=True)
    room_id = Column(Uuid, ForeignKey("rooms.id"))

    room = relationship("Room", back_populates="persons")
    contacts = relationship("Contact", back_populates="person")


class ContentType(enum.Enum):
    github = "github"
    twitter = "twitter"
    facebook = "facebook"
    instagram = "instagram"
    linkedin = "linkedin"
    email = "email"
    url = "url"


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Uuid, primary_key=True, index=True)
    person_id = Column(Uuid, ForeignKey("persons.id"))
    content = Column(String(32), index=True)
    content_type = Column(Enum(ContentType))

    person = relationship("Person", back_populates="contacts")
