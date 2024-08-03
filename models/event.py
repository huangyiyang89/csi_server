import time
from sqlmodel import SQLModel, Field, Relationship
from pydantic import computed_field
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.camera import Camera
    from models.eventtype import EventType

class EventBase(SQLModel):
    area_name: str | None = None
    image_url: str | None = None
    timestamp: int | None = int(time.time())
    uploaded: bool | None = False
    camera_id: int | None = Field(default=None, foreign_key="camera.id")
    eventtype_id: str | None = Field(default=None, foreign_key="eventtype.id")

    @computed_field
    @property
    def localtime(self) -> str:
        local_time_str = time.strftime(
            r"%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp)
        )
        return local_time_str

class Event(EventBase, table=True):
    id: int = Field(primary_key=True)
    camera: "Camera" = Relationship(back_populates="events")
    eventtype: "EventType" = Relationship()


class EventCreate(EventBase):
    pass





class EventUpdate(SQLModel):
    area_name: str | None = None
    image_url: str | None = None
    timestamp: int | None = int(time.time())
    uploaded: bool | None = None
    camera_id: int | None = None
    eventtype_id: str | None = None
