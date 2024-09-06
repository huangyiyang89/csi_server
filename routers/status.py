import util
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session, select
from models.camera import Camera
from models.nvr import Nvr
router = APIRouter(prefix="/api/status")

@router.get("/")
async def get_status(*,session: Session = Depends(get_session)):


    nvrs = session.exec(select(Nvr)).all()
    for nvr in nvrs:
        state = await util.check_status(nvr.ip)
        nvr.state = state
    
    

    cameras = session.exec(select(Camera)).all()
    for camera in cameras:
        state = await util.check_status(camera.ip_addr)
        camera.state = state


    session.commit()


    mac = util.get_local_mac()
    ip = util.get_ip_address()
    cpu = util.get_cpu_percent()
    npu = util.get_npu_percent()
    mem = util.get_memory_percent()
    disk = util.get_disk_percent()
    uptime = util.get_uptime()
    return {
        "mac": mac,
        "ip": ip,
        "cpu": cpu,
        "npu": npu,
        "mem": mem,
        "disk": disk,
        "uptime": uptime
    }