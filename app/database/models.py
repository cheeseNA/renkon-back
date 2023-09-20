from sqlalchemy import Column, ForeignKey, Integer, String, Uuid, DateTime, Enum
from sqlalchemy.orm import relationship
import enum


from .database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Uuid, primary_key=True, index=True)
    ref_code = Column(String(6), index=True)
    created_at = Column(DateTime)
    close_at = Column(DateTime)

    persons = relationship("Person", back_populates="room")
    open_rooms = relationship("OpenRoom", back_populates="rooms")
    closed_rooms = relationship("ClosedRoom", back_populates="rooms")


class OpenRoom(Base):
    __tablename__ = "open_rooms"

    id = Column(Uuid, ForeignKey("rooms.id"), primary_key=True, index=True)

    rooms = relationship("Room", back_populates="open_rooms")


class ClosedRoom(Base):
    __tablename__ = "closed_rooms"

    id = Column(Uuid, ForeignKey("rooms.id"), primary_key=True, index=True)

    rooms = relationship("Room", back_populates="closed_rooms")


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    content = Column(String(32), index=True)
    content_type = Column(Enum(ContentType))

    person = relationship("Person", back_populates="contacts")
