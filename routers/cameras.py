from typing import Optional
import requests
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import RedirectResponse,StreamingResponse
from sqlmodel import Session
from database import get_session, select
from models.camera import Camera, CameraCreate, CameraUpdate
from models.schema import CameraWithDatas
from task import sign


router = APIRouter(prefix="/api/cameras", tags=["cameras"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_camera(
    *, camera: CameraCreate, session: Session = Depends(get_session)
) -> CameraWithDatas:
    db_camera = Camera(**camera.model_dump())
    session.add(db_camera)
    session.commit()
    session.refresh(db_camera)
    return db_camera


@router.patch("/{camera_id}")
async def patch_camera(
    *, camera_id: int, camera: CameraUpdate, session: Session = Depends(get_session)
) -> CameraWithDatas:
    db_camera = session.get(Camera, camera_id)
    if not db_camera:
        raise HTTPException(status_code=404)
    for key, value in camera.model_dump(exclude_unset=True).items():
        setattr(db_camera, key, value)
    session.commit()
    session.refresh(db_camera)
    return db_camera


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(*, camera_id: int, session: Session = Depends(get_session)):
    db_camera = session.get(Camera, camera_id)
    if not db_camera:
        raise HTTPException(status_code=404)
    session.delete(db_camera)
    session.commit()
    return None


@router.get("/{camera_id}")
async def get_camera(
    *, camera_id: int, session: Session = Depends(get_session)
) -> CameraWithDatas:
    camera = session.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404)
    # 取最后10条
    # camera.events = sorted(camera.events, key=lambda x: x.id, reverse=True)[:10]
    return camera


@router.get("/")
async def get_cameras(
    *, session: Session = Depends(get_session)
) -> list[CameraWithDatas]:
    cameras_with_limit_events = []
    cameras = session.exec(select(Camera)).all()
    for camera in cameras:
        camera_with_events = CameraWithDatas.model_validate(camera)
        camera_with_events.events = []
        events = (
            session.exec(select(Camera).where(Camera.id == camera.id))
            .first()
            .events[:10]
        )
        for event in events:
            camera_with_events.events.append(event)
        cameras_with_limit_events.append(camera_with_events)

    return cameras_with_limit_events


@router.get("/{camera_id}/url")
async def get_url(*, camera_id: int,time:Optional[str] = "",session: Session = Depends(get_session)):
    camera = session.get_one(Camera, camera_id)
    if not camera or not camera.nvr or not camera.nvr_channel:
        raise HTTPException(status_code=404, detail="Camera not found or incomplete configuration")

    try:
        url = f"http://localhost:8080/video/api/pull?ip={camera.nvr.ip}&ch={camera.nvr_channel}&sign={sign()}&time={time}"
        response = requests.get(url)
        response.raise_for_status()
        data:dict = response.json()
        if data.get("code") != 200 or "flv" not in data.get("data", {}):
            return RedirectResponse(url="/error.flv")

        return RedirectResponse(url=data["data"]["flv"])
    except Exception as e:
        return RedirectResponse(url="/error.flv")
    