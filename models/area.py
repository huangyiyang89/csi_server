import time
from sqlmodel import SQLModel, Field, Relationship
from pydantic import computed_field
from typing import TYPE_CHECKING, Optional
from models.algoparam import AlgoParam,AlgoParamCreate

if TYPE_CHECKING:
    from models.camera import Camera



class AreaBase(SQLModel):
    name: str
    camera_id: int = Field(foreign_key="camera.id")
    coordinates: str | None = "[]"
    timestamp: int | None = int(time.time())

    @computed_field
    @property
    def localtime(self) -> str:
        local_time_str = time.strftime(
            r"%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp)
        )
        return local_time_str


class Area(AreaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    camera: "Camera" = Relationship(back_populates="areas")
    algoparam: Optional["AlgoParam"] = Relationship(cascade_delete=True)


class AreaCreate(AreaBase):
    algoparam: Optional["AlgoParam"] | None = None


class AreaUpdate(SQLModel):
    name: str | None = None
    coordinates: str | None = None
    algoparam: Optional["AlgoParam"] | None = None
    timestamp: int | None = int(time.time())
