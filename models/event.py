import time
from sqlmodel import SQLModel, Field, Relationship
from models.camera import Camera, CameraPublic
from models.eventtype import EventType



class EventBase(SQLModel):
    name: str
    area_name: str | None = None
    image_url: str | None = None
    timestamp: int | None = int(time.time())
    uploaded: bool | None = False
    camera_id: int | None = Field(default=None, foreign_key="camera.id")
    eventtype_id: str | None = Field(default=None, foreign_key="eventtype.id")


class Event(EventBase, table=True):
    id: int = Field(primary_key=True)
    camera: Camera = Relationship(back_populates="events")
    eventtype: EventType = Relationship()


class EventCreate(EventBase):
    pass


class EventPublic(EventBase):
    id: int
    camera: CameraPublic = Relationship(back_populates="events")
    eventtype: EventType = Relationship()


class EventUpdate(SQLModel):
    name: str | None = None
    area_name: str | None = None
    image_url: str | None = None
    timestamp: int | None = int(time.time())
    uploaded: bool | None = None
    camera_id: int | None = None
    eventtype_id: str | None = None
