from fastapi import APIRouter, HTTPException,Depends
from sqlmodel import Session, select
from database import get_session
from models.area import Area, AreaCreate, AreaPublic, AreaUpdate,AreaWithDatas

router = APIRouter(
    prefix="/areas",
    tags=["areas"],
    responses={404: {"description": "Not found"}},
)


@router.post("/",response_model=AreaWithDatas)
def create_area(area: AreaCreate, session: Session = Depends(get_session)):
    db_area = Area(**area.model_dump())
    session.add(db_area)
    session.commit()
    session.refresh(db_area)
    return area

@router.get("/",response_model=list[AreaWithDatas])
def get_areas(*,camera_id: int | None = None,session: Session = Depends(get_session)):
    query = select(Area)
    if camera_id:
        query = query.where(Area.camera_id == camera_id)
    areas = session.exec(query).all()
    return areas


@router.get("/{area_id}",response_model=AreaPublic)
def get_area(*,area_id: int, session: Session = Depends(get_session)):
    return session.get(Area, area_id)

@router.patch("/{area_id}", response_model=AreaPublic)
def update_area(*,area_id: int, area: AreaUpdate, session: Session = Depends(get_session)):
    db_area = session.get(Area, area_id)
    if not db_area:
        raise HTTPException(status_code=404)
    for key, value in area.model_dump().items():
        setattr(db_area, key, value)
    session.add(db_area)
    session.commit()
    session.refresh(db_area)
    return db_area

@router.delete("/{area_id}")
def delete_area(*,area_id: int, session: Session = Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    session.delete(area)
    session.commit()
    return {"message": "Area deleted successfully"}
    