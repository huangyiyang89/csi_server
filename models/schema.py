from models.camera import CameraBase
from models.area import AreaBase
from models.algoparam  import AlgoParamBase
from models.event import EventBase
from models.eventtype import EventType
from models.nvr import Nvr

class CameraPublic(CameraBase):
    id: int

class AreaPublic(AreaBase):
    id: int

class AlgoParamPublic(AlgoParamBase):
    id: int

class AreaWithDatas(AreaPublic):
    camera: CameraPublic
    algoparam: AlgoParamPublic | None = None


class EventPublic(EventBase):
    id: int
    camera: CameraPublic | None = None
    eventtype: EventType | None = None

class CameraWithDatas(CameraPublic):
    nvr: Nvr | None = None
    areas: list[AreaWithDatas] | None = []
    events: list[EventPublic] | None = []
    live_url: str | None = None