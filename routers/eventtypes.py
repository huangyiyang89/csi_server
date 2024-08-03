from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models.eventtype import EventType


router = APIRouter(
    prefix="/api/eventtypes",
    tags=["eventtypes"]
)


@router.get("/")
def get_event_types(*, session: Session = Depends(get_session)):
    return session.exec(select(EventType)).all()


@router.get("/{eventtype_id}")
def get_event_type(*, eventtype_id: int, session: Session = Depends(get_session)):
    eventtype = session.get(EventType, eventtype_id)
    if not eventtype:
        raise HTTPException(status_code=404)
    return eventtype
