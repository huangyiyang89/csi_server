import uvicorn
from database import create_db_and_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers.users import router as users_router
from routers.eventtypes import router as eventtypes_router
from routers.algoparams import router as algoparams_router
from routers.events import router as events_router
from routers.areas import router as areas_router
from routers.cameras import router as cameras_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan, 
    responses={404: {"description": "Not found"}}
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
