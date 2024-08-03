import time,random
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, desc
from database import get_session
from models.event import Event
from models.camera import Camera
from models.schema import EventPublic


router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("/", response_model=list[EventPublic])
def get_events(
    *,
    offset=0,
    limit=1000,
    start_time=0,
    end_time=9999999999,
    session: Session = Depends(get_session)
):
    statement = (
        select(Event)
        .where(Event.timestamp >= start_time, Event.timestamp <= end_time)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Event.id))
    )
    results = session.exec(statement)
    return results.all()

@router.get("/live", response_model=list[EventPublic])
def get_live_events(
    *,
    session: Session = Depends(get_session)
):
    cameras = session.exec(select(Camera)).all()
    all_events: list[Event] = []
    for camera in cameras:
        statement = (
            select(Event)
            .where(Event.camera_id == camera.id)
            .order_by(desc(Event.timestamp))
            .limit(10)
            )
        events = session.exec(statement).all()
        all_events.extend(events)
    return all_events

@router.get("/gen")
def generate_random_events(*, count: int = 5,session: Session = Depends(get_session)):
    cameras: list[Camera] = session.exec(select(Camera)).all()  
    for camera in cameras:
        for i in range(count):
            t = int(time.time()) - random.randint(0, 86400) * i
            a = "区域" + str(random.randint(1, count))
            ran_eventtype_id = random.choice(
                [
                    "1201",
                    "1202",
                    "1401",
                    "1501",
                    "2101",
                    "2102",
                    "3101",
                    "1402",
                    "1502",
                    "1311",
                ]
            )
            new_event = Event(
                camera_id=camera.id,
                area_name=a,
                eventtype_id=ran_eventtype_id,
                timestamp=t,
                image_url="images/event" + str(random.randint(1, 4)) + ".jpg",
                uploaded=True,
            )
            session.add(new_event)
    session.commit()
    return None