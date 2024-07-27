import time
from sqlmodel import Field, Relationship, SQLModel
from models.camera import Camera, CameraPublic
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.algoparam import AlgoParam, AlgoParamPublic, AlgoParamUpdate



class AreaBase(SQLModel):
    name: str
    coordinates: str | None = None
    timestamp: int | None = int(time.time())
    camera_id: int = Field(foreign_key="camera.id")


class Area(AreaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    camera: Camera = Relationship(back_populates="areas")
    algoparams: list["AlgoParam"] = Relationship(back_populates="area")


class AreaPublic(AreaBase):
    id: int


class AreaWithDatas(AreaPublic):
    camera: CameraPublic
    algoparams: list["AlgoParamPublic"] = Relationship(back_populates="area")


class AreaCreate(AreaBase):
    pass


class AreaUpdate(SQLModel):
    name: str | None = None
    coordinates: str | None = None
    algoparams: list["AlgoParamUpdate"] | None = Relationship(back_populates="area")
    timestamp: int | None = int(time.time())
