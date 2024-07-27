import time
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.area import Area, AreaPublic
    from models.event import Event, EventPublic

class CameraBase(SQLModel):
    name: str
    ip_addr: str
    mac: str
    frame_width: int
    frame_height: int
    description: str | None = ""
    state: int | None = 0
    timestamp: int | None = int(time.time())


class Camera(CameraBase, table=True):
    id: int = Field(default=None, primary_key=True)
    areas: list["Area"] | None = Relationship(back_populates="camera")
    events: list["Event"] | None = Relationship(back_populates="camera")


class CameraPublic(CameraBase):
    id: int


class CameraWithDatas(CameraPublic):
    areas: list["AreaPublic"] | None = Relationship(back_populates="camera")
    events: list["EventPublic"] | None = Relationship(back_populates="camera")


class CameraCreate(CameraBase):
    pass


class CameraUpdate(SQLModel):
    name: str | None = None
    ip_addr: str | None = None
    mac: str | None = None
    description: str | None = None
    frame_height: int | None = None
    frame_width: int | None = None
    state: int | None = None
    timestamp: int | None = int(time.time())
