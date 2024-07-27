from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models.event import Event,EventPublic

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.get("/",response_model=list[EventPublic])
def get_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()
