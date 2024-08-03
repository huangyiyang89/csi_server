from sqlmodel import Field,Relationship, SQLModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.area import Area


class AlgoParamBase(SQLModel): 
    area_id: int | None = Field(default=None,foreign_key="area.id")
    eventtype_ids: str | None = "[]"
    nms_thresh: float | None = 0.9
    people_score_thresh: float | None = 0.9
    face_score_thresh: float | None = 0.9
    head_score_thresh: float | None = 0.9
    helmet_score_thresh: float | None = 0.9
    fire_score_thresh: float | None = 0.9
    water_score_thresh: float | None = 0.9
    falldown_score_thresh: float | None = 0.9
    cross_line:str | None = "[]"
    cross_direction:str | None = "[]"
    iou_cost_weight: float | None = 0.9
    cost_th: float | None = 0.9
    max_mismatch_times:int | None = 5

class AlgoParam(AlgoParamBase, table=True): 
    id: int = Field(default=None, primary_key=True)
    area: "Area" = Relationship(back_populates="algoparam")

class AlgoParamCreate(AlgoParamBase):
    pass

class AlgoParamUpdate(SQLModel):
    eventtype_ids: str | None = None
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