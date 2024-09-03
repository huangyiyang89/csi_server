from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from database import get_session, select
from models.nvr import Nvr, NvrUpdate, NvrCreate


router = APIRouter(prefix="/api/nvrs", tags=["nvrs"])


@router.get("/")
async def get_nvr(*, session: Session = Depends(get_session)) -> list[Nvr]:
    return session.exec(select(Nvr)).all()


@router.get("/{nvr_id}")
async def get_nvr(*, nvr_id: int, session: Session = Depends(get_session)) -> Nvr:
    return session.get(Nvr, nvr_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_nvr(
    *, nvr: NvrCreate, session: Session = Depends(get_session)
) -> Nvr:
    db_nvr = Nvr(**nvr.model_dump())
    session.add(db_nvr)
    session.commit()
    session.refresh(db_nvr)
    return db_nvr


@router.patch("/{nvr_id}")
async def patch_nvr(
    *, nvr_id: int, nvr: NvrUpdate, session: Session = Depends(get_session)
) -> Nvr:
    db_nvr = session.get(Nvr, nvr_id)
    if not db_nvr:
        raise HTTPException(status_code=404)

    for key, value in nvr.model_dump(exclude_unset=True).items():
        setattr(db_nvr, key, value)

    session.commit()
    session.refresh(db_nvr)
    return db_nvr

@router.delete("/{nvr_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nvr(*, nvr_id: int, session: Session = Depends(get_session)):
    db_nvr = session.get(Nvr, nvr_id)
    if not db_nvr:
        raise HTTPException(status_code=404)
    session.delete(db_nvr)
    session.commit()
    return None

