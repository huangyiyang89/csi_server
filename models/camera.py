import time
from sqlmodel import SQLModel, Field, Relationship
from pydantic import computed_field
from typing import TYPE_CHECKING
from models.nvr import Nvr

if TYPE_CHECKING:
    from models.area import Area, AreaPublic
    from models.event import Event, EventPublic


class CameraBase(SQLModel):
    name: str
    ip_addr: str
    mac: str
    brand: str
    frame_width: int
    frame_height: int
    description: str | None = ""
    state: int | None = 0
    timestamp: int | None = int(time.time())
    nvr_id: int | None = Field(default=None, foreign_key="nvr.id")
    nvr_channel: str | None = None

    @computed_field
    @property
    def localtime(self) -> str:
        local_time_str = time.strftime(
            r"%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp)
        )
        return local_time_str


class Camera(CameraBase, table=True):
    id: int = Field(default=None, primary_key=True)
    nvr: Nvr  = Relationship()
    areas: list["Area"] | None = Relationship(
        back_populates="camera", cascade_delete=True
    )
    events: list["Event"] | None = Relationship(back_populates="camera")


class CameraCreate(CameraBase):
    pass


class CameraUpdate(SQLModel):
    name: str | None = None
    ip_addr: str | None = None
    mac: str | None = None
    nvr_channel: str | None = None
    description: str | None = None
    frame_height: int | None = None
    frame_width: int | None = None
    state: int | None = None
    timestamp: int | None = int(time.time())
    nvr_id: int | None = None
