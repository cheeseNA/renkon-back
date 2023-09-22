import datetime
import uuid

from pydantic import BaseModel, field_validator

from app.database.models import ContentType


class Contact(BaseModel):
    id: int
    person_id: int
    content: str
    content_type: ContentType

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    person_id: int
    content: str
    content_type: ContentType

    @field_validator("content")
    def content_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("content must not be empty")
        return v


class PersonCreate(BaseModel):
    name: str
    room_id: uuid.UUID

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("name must not be empty")
        return v


class Person(BaseModel):
    id: int
    name: str
    room_id: uuid.UUID
    contacts: list[Contact] = []

    class Config:
        from_attributes = True


class Room(BaseModel):
    id: uuid.UUID
    ref_code: str
    created_at: datetime.datetime
    close_at: datetime.datetime
    persons: list[Person] = []

    class Config:
        from_attributes = True


class RoomCreate(BaseModel):
    duration: datetime.timedelta

    @field_validator("duration")
    def duration_must_be_positive(cls, v):
        if v <= datetime.timedelta():
            raise ValueError("duration must be positive")
        return v

    @field_validator("duration")
    def duration_must_be_less_than_3_days(cls, v):
        if v > datetime.timedelta(days=3):
            raise ValueError("duration must be less than 3 days")
        return v
