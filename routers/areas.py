from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from database import get_session

from models.area import Area, AreaCreate, AreaUpdate
from models.camera import Camera
from models.algoparam import AlgoParam
from models.schema  import AreaWithDatas



router = APIRouter(prefix="/api/areas", tags=["areas"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_area(*, area: AreaCreate, session: Session = Depends(get_session)) -> AreaWithDatas:


    db_area = Area.model_validate(area)
    db_camera = session.get(Camera, area.camera_id)
    if not db_camera:
        raise HTTPException(
            status_code=404, detail=f"Camera with id {area.camera_id} not found"
        )
    session.add(db_area)
    session.commit()
    session.refresh(db_area)
    return db_area


@router.get("/", response_model=list[AreaWithDatas])
def get_areas(*, camera_id: int | None = None, session: Session = Depends(get_session)):
    statement = select(Area)
    if camera_id:
        statement = statement.where(Area.camera_id == camera_id)
    areas = session.exec(statement).all()
    return areas


@router.get("/{area_id}", response_model=AreaWithDatas)
def get_area(*, area_id: int, session: Session = Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=404)
    return area


@router.patch("/{area_id}", response_model=AreaWithDatas)
def patch_area(
    *, area_id: int, area: AreaUpdate, session: Session = Depends(get_session)
):
    db_area = session.get(Area, area_id)
    if not db_area:
        raise HTTPException(status_code=404)

    for key, value in area.model_dump(exclude="algoparam", exclude_unset=True).items():
        setattr(db_area, key, value)

    if area.algoparam:
        db_algoParam = AlgoParam(**area.algoparam.model_dump())
        db_area.algoparam = db_algoParam

    session.commit()
    session.refresh(db_area)
    return db_area


@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area(*, area_id: int, session: Session = Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=404)
    session.delete(area)
    session.commit()
    return None
