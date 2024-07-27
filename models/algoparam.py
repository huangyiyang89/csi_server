from sqlmodel import Field, Relationship, SQLModel
from models.area import Area
from models.eventtype import EventType

class AlgoParamBase(SQLModel):  
    area_id: int = Field(foreign_key="area.id")
    eventtype_id: str = Field(foreign_key="eventtype.id")
    nms_thresh: float | None = None
    people_score_thresh: float | None = None
    face_score_thresh: float | None = None
    head_score_thresh: float | None = None
    helmet_score_thresh: float | None = None
    fire_score_thresh: float | None = None
    water_score_thresh: float | None = None
    falldown_score_thresh: float | None = None
    cross_line:str | None = None
    cross_direction:str | None = None
    iou_cost_weight: float | None = None
    cost_th: float | None = None
    max_mismatch_times:int | None = None

class AlgoParam(AlgoParamBase, table=True):
    id: int = Field(default=None, primary_key=True)
    area: Area = Relationship(back_populates="algoparams")
    eventtype: EventType = Relationship()


class AlgoParamPublic(AlgoParamBase):
    id: int = Field(default=None, primary_key=True)

class AlgoParamCreate(AlgoParamBase):
    pass

class AlgoParamUpdate(SQLModel):
    nms_thresh: float | None = None
    people_score_thresh: float | None = None
    face_score_thresh: float | None = None
    head_score_thresh: float | None = None
    helmet_score_thresh: float | None = None
    fire_score_thresh: float | None = None
    water_score_thresh: float | None = None
    falldown_score_thresh: float | None = None
    cross_line:str | None = None
    cross_direction:str | None = None
    iou_cost_weight: float | None = None
    cost_th: float | None = None
    max_mismatch_times:int | None = None