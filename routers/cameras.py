from fastapi import APIRouter, status,HTTPException,Depends
from sqlmodel import Session, select
from database import get_session
from models.camera import Camera, CameraPublic, CameraCreate, CameraUpdate, CameraWithDatas

router = APIRouter(
    prefix="/cameras",
    tags=["cameras"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CameraWithDatas,status_code=status.HTTP_201_CREATED)
async def create_camera(camera: CameraCreate, session: Session = Depends(get_session)):
    db_camera = Camera(**camera.model_dump())
    session.add(db_camera)
    session.commit()
    session.refresh(db_camera)
    return db_camera


@router.patch("/{camera_id}",response_model=CameraWithDatas)
async def patch_camera(camera_id: int, camera: CameraUpdate, session: Session = Depends(get_session)):
    db_camera = session.get(Camera, camera_id)
    if not db_camera:
        raise HTTPException(status_code=404)
    for key, value in camera.model_dump(exclude_unset=True).items():
        setattr(db_camera, key, value)
    session.commit()
    session.refresh(db_camera)
    return db_camera



@router.delete("/{camera_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(camera_id: int, session: Session = Depends(get_session)):
    db_camera = session.get(Camera, camera_id)
    if not db_camera:
        raise HTTPException(status_code=404)
    session.delete(db_camera)
    session.commit()
    return {"message": "deleted"}


@router.get("/{camera_id}",response_model=CameraWithDatas)
async def get_camera(camera_id: int, session: Session = Depends(get_session)):
    camera = session.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404)
    return camera


@router.get("/",response_model=list[CameraWithDatas])
async def get_cameras(session: Session = Depends(get_session)):
    cameras = session.exec(select(Camera)).all()
    return cameras