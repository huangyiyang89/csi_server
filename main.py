import uvicorn
import os
import util
import config
from apscheduler.schedulers.background import BackgroundScheduler
from database import create_db_and_tables
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from routers.users import router as users_router
from routers.eventtypes import router as eventtypes_router
from routers.algoparams import router as algoparams_router
from routers.events import router as events_router
from routers.areas import router as areas_router
from routers.cameras import router as cameras_router
from routers.nvrs import router as nvrs_router
from routers.status import router as status_router


def status_task():
    """10分钟执行一次"""
    from task import upload_status, upload_events
    upload_status()
    upload_events()


def message_task():
    """10秒钟执行一次"""
    from task import get_tasks
    tasks = get_tasks()

    try:
        for task in tasks:
            if task["action"] == "reboot":
                util.reboot()
            if task["action"] == "web":
                params = task["params"]
                host = params["host"]
                port = params["port"]
                timeout = params["timeout"]
                util.start_ssh_process(
                    host,
                    port,
                    80,
                    config.ssh_username,
                    config.ssh_password,
                    timeout=timeout,
                )
            if task["action"] == "ssh":
                params = task["params"]
                host = params["host"]
                port = params["port"]
                timeout = params["timeout"]
                util.start_ssh_process(
                    host,
                    port,
                    22,
                    config.ssh_username,
                    config.ssh_password,
                    timeout=timeout,
                )
            if task["action"] == "video":
                pass
    except Exception as e:
        print("Run task error:", e)

scheduler = BackgroundScheduler()
scheduler.add_job(status_task, "interval", seconds=600)
scheduler.add_job(message_task, "interval", seconds=10)
scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan, responses={404: {"description": "Not found"}})
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(eventtypes_router)
app.include_router(algoparams_router)
app.include_router(events_router)
app.include_router(areas_router)
app.include_router(cameras_router)
app.include_router(nvrs_router)
app.include_router(status_router)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.serve_port)
