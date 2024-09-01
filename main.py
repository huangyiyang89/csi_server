import uvicorn
import os
import asyncio
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
from asyncio.windows_events import ProactorEventLoop


class ProactorServer(uvicorn.Server):
    def run(self, sockets=None):
        loop = ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.serve(sockets=sockets))


def status_task():
    """10分钟执行一次"""
    print("---------------------status_task triggered---------------------")
    from platform_service import upload_status, upload_events
    upload_status()
    print()
    upload_events()
    print()
 
    


def message_task():
    """10秒钟执行一次"""
    print("---------------------message_task triggered---------------------")
    from platform_service import get_tasks
    tasks = get_tasks()
    for task in tasks:
        pass
    print()
    



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

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/{full_path:path}")
async def serve_react_app(request: Request, full_path: str):
    static_files_dir = "frontend"
    file_path = os.path.join(static_files_dir, full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(static_files_dir, "index.html"))


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8001)
    # 启用proactor loop
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, reload=False)
    server = ProactorServer(config=config)
    server.run()
